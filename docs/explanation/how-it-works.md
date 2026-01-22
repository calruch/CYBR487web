# How it works

This overview is based on the `main.py` and `src/networkScanner.py` implementation in the snapshot.

## High-level flow

1. Parse CLI args (`ParseClass` in `src/argParser.py`)
2. Print scan start info (`Report.print_scan_start`)
3. (When `scanType=all` or `scanType=SelfScan`) run **Self Scan**
4. Discover hosts:
   - **ARP scan** (`ARPHostIdentifier.ArpScan`) *or*
   - **ICMP-based host identification** (`ICMPHostScanner.activeHostScan`)
5. For each host found:
   - (Optional) **OS fingerprinting** via ICMP IPID behavior (`ICMPHostIdentifier.scan`)
   - (Optional) **TCP SYN port scan** (`TCPPortScanner.scan`)
   - (Optional) **Traceroute** (`TraceRouteScanner`)
   - Store results in `HostStorage`
   - Print a per-host report box
6. Print final scan summary

## OS fingerprinting (ICMP IPID behavior)

The ICMP OS detector sends ICMP packets and inspects returned IPID sequences:

- **Global incrementing** → "Windows or FreeBSD"
- **Bucket/increasing pattern** → "Linux"
- **PRNG-like pattern** → "MacOS or IOS"
- Otherwise → "Unknown OS"

!!! note "Heuristic"
    This is a heuristic. NAT, middleboxes, firewalls, and some host configurations can distort results.

## Port scanning (TCP SYN)

Ports are scanned using a TCP SYN probe:

- SYN-ACK indicates open → the scanner sends an RST to close
- RST-ACK indicates closed
- No response is treated as closed/filtered (depends on network behavior)

## Traceroute

Traceroute collects hop IPs up to `--maxhops`, recording `*` for timeouts.

Two modes are supported in the snapshot:

- ICMP traceroute
- TCP traceroute
