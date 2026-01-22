# How It Works

This section describes what the program *actually does* at runtime, based on the current implementation in `src/main.py` and `src/networkScanner.py`.

## High-level flow

1. **Parse arguments** (`src/argParser.py`)
2. **Initialize reporting** (`src/generateReport.py`)
3. Optional: **Self Scan** (for `scanType=all` and `SelfScan`)
4. **Host discovery** (ARP or ICMP)
5. For each discovered host:
   - Optional: **OS detection** (ICMP)
   - Optional: **TCP port scan** (SYN)
   - Optional: **Traceroute** (TCP and/or ICMP)
   - **Print a host report**
6. Print a final **scan summary**

## Self Scan

Self Scan reads `/proc/net/tcp` and `/proc/net/udp`, then maps socket inodes back to processes by walking `/proc/<pid>/fd`.

Current filtering behavior:

- TCP entries: includes sockets where the `/proc/net/tcp` state is `0A` (LISTEN)
- UDP entries: includes sockets where the `/proc/net/udp` state is `07`

Output is printed as a list of process names and their local/remote socket endpoints.

## Host discovery

Choose the host discovery method with `--hostid`:

- `--hostid=ARP` (default): sends ARP requests across the target network and returns `(ip, mac)` for responders.
- `--hostid=ICMP`: expands the CIDR to individual hosts and sends ICMP echo requests.

## OS detection

When `scanType` is `all` or `ICMP`, the program calls an ICMP-based OS fingerprinting routine (`ICMPHostIdentifier.scan`).
If OS detection returns no result, the program records the OS as "Unknown".

## TCP port scanning

When `scanType` is `all` or `TCP`, the program performs a TCP SYN scan (`TCPPortScanner.scanPort`).

- Sends a SYN packet to each requested port.
- Marks the port "open" if it receives a SYN-ACK.
- Sends an RST packet to cleanly close the half-open connection.

## Traceroute

When `scanType` is:

- `all` or `TraceRouteTCP`: runs a TCP traceroute
- `all` or `TraceRouteICMP`: runs an ICMP traceroute

The traceroute implementation stops early after a small number of consecutive no-responses.

## Output

Output is written to STDOUT and formatted using `src/generateReport.py`.

- With `--verbose`, you will see additional status lines (e.g., "Running ARP scan…", "Detecting OS…").
- The `--moreverbose` flag is currently parsed but not used to change output.
