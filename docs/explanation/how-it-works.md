# How it works

This document describes what the code does today, grounded in the current Python modules:

- `argParser.py` — CLI parsing and validation
- `networkScanner.py` — ARP/ICMP host discovery, OS heuristic, SYN scan, traceroute
- `selfScan.py` — local `/proc` scan
- `generateReport.py` — formatted console output
- `main.py` — orchestration

## 1) Argument parsing

`ParseClass.buildParser()` defines the CLI surface. `ParseClass.parser()` then converts those raw args into:

- `ipList` — a **CIDR string**, e.g. `"192.168.1.0/24"` or `"192.168.1.10/32"`
- `portList` — a list of integers, or `None`
- `timeoutVal` — integer seconds (default `5`)
- `verbose`, `moreverbose` — booleans (`moreverbose` is currently unused)
- `scanType` — numeric internal mode:
  - `1` all
  - `2` ICMP (OS heuristic)
  - `3` TCP (SYN scan)
  - `4` TraceRouteTCP
  - `5` TraceRouteICMP
  - `6` SelfScan
- `hostID` — numeric host discovery mode:
  - `1` ARP
  - `2` ICMP
  - `0` NONE

Important behaviors:

- `--network` is required for all scan types **except** `SelfScan`.
- `--ports` is required when `--scanType` includes TCP port scanning (`all` or `TCP`).
- `-h/--help` is parsed but not implemented as a real help output.

## 2) Self scan (local `/proc`)

When `scanType` is `all` or `SelfScan`, `main.py` runs `SelfScan.get_net_processes()`:

- Enumerates `/proc/<pid>/fd/*` symlinks to find socket inodes
- Parses `/proc/net/tcp` and `/proc/net/udp`
- Correlates inode → `(protocol, local_ip, local_port, remote_ip, remote_port)`
- Filters to:
  - TCP state `0A` (LISTEN)
  - UDP state `07`

Notes:

- The current implementation keeps **at most one** connection tuple per process name (later matches overwrite earlier ones).
- Accessing other users’ `/proc/<pid>/fd` entries often requires elevated privileges.

## 3) Host discovery

Host discovery is chosen via `--hostid`:

### ARP (`--hostid=ARP`)

`ARPHostIdentifier.ArpScan()` uses Scapy `srp()` to broadcast ARP requests.

- Works best on the local L2 segment (same broadcast domain)
- Returns a list of `(ip, mac)` tuples

### ICMP (`--hostid=ICMP`)

`ICMPHostScanner.activeHostScan()` expands the CIDR and sends ICMP Echo Requests.

- Returns a list of `(ip, None)` tuples for responsive hosts
- This is **host discovery**, not the OS heuristic

### NONE (`--hostid=NONE`)

Skips host discovery.

- In `main.py`, this mode is effectively intended for traceroute-only runs.
- If you pass a broad CIDR with traceroute-only, the traceroute scanner will expand it and attempt a trace for each host.

## 4) Per-host scanning

For each discovered host, `main.py` may run up to three actions depending on `--scanType`:

### OS heuristic (`--scanType=all` or `--scanType=ICMP`)

`ICMPHostIdentifier.scan()` sends ICMP packets and inspects the returned IPID values.

It classifies the target as one of:

- **Windows or FreeBSD** (globally incrementing IPID pattern)
- **Linux** (monotonic/bucket-like behavior)
- **MacOS or iOS** (PRNG-like behavior)
- **Unknown OS**

This is a heuristic and can be influenced by network devices, rate limiting, firewalls, and OS hardening.

### TCP SYN port scan (`--scanType=all` or `--scanType=TCP`)

`TCPPortScanner.scanPort()`:

- Sends a TCP SYN packet to each target port
- Treats SYN-ACK as **open** and sends a RST to close
- Treats RST-ACK or no response as **closed/filtered**

### Traceroute (`--scanType=all` or `TraceRoute*`)

`TraceRouteScanner.TCPtrace()`:

- Sends TCP SYN to destination port `80`
- Increases TTL from 1…`maxhops`
- Stops early after consecutive timeouts or when a terminal response is reached

`TraceRouteScanner.ICMPtrace()`:

- Uses ICMP Echo with TTL increments

Implementation notes:

- If the first two hops are timeouts (`*`), `checkTraceResults()` returns `None` and the report prints a “no results” note.
- ICMP traceroute records `*` hops without an RTT value in one code path; this can lead to formatting issues when printing those results.

## 5) Storage and reporting

Results are accumulated in `HostStorage` (a list of dictionaries) and printed via `Report`:

- Start-of-scan banner
- Optional self scan results
- Per-host scan output
- Optional port scan output
- Optional traceroute output
- End-of-scan summary

See **output.md** for details.
