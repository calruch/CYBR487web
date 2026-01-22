# Design and limitations

This document describes known constraints and limitations based on the current code.

## Platform and permissions

- **Linux required for SelfScan:** `selfScan.py` reads `/proc` and `/proc/net/*`.
- **Elevated privileges often required:** Scapy raw packet operations (ARP, ICMP, SYN scan, traceroute) typically require root/admin privileges.

## CLI limitations

- `-h/--help` is parsed but does not print usage output.
- `--ports` accepts a single string value (single, comma list, or range). Space-separated ports are not supported.

## Scanning limitations

- **ARP discovery scope:** ARP discovery is limited to the local broadcast domain.
- **OS identification is heuristic:** The ICMP/IPID method can be unreliable when IPID is randomized, traffic is rate-limited, or middleboxes interfere.
- **TCP traceroute uses destination port 80:** This is currently fixed in the implementation.
- **ICMP traceroute formatting edge case:** ICMP traceroute may record timeout hops without RTT values in one code path, which can cause formatting issues when printed.

## Data and reporting

- Results are printed to the console and kept in memory; there is no built-in JSON export or file output.
- Per-host output is split across sections (host info, ports, traceroute), rather than a single combined host report.

## Codebase notes

- `traceNode.py` contains a linked-list traceroute path representation, but it is incomplete (e.g., `rotatePath()` is a stub) and is not currently used by `main.py`.

## Practical improvements (not implemented)

These are not implemented today, but are reasonable next steps:

- Implement real CLI help output via argparse’s default help behavior
- Add JSON output and/or report files
- Improve SelfScan to report multiple sockets per process
- Make traceroute configuration (destination port, retry counts) user-configurable
