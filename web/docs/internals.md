# Internals

## High-level flow

1. Parse CLI args
2. Print scan start report
3. If scanType is `all` or `SelfScan`:
   - run Self Scan
   - if `SelfScan`, exit early
4. Discover hosts:
   - ARP discovery or ICMP discovery (depends on `--hostid`)
5. Per host:
   - OS fingerprinting (ICMP IPID heuristic) when enabled
   - TCP SYN port scanning when enabled
   - Traceroute (ICMP or TCP) when enabled
6. Print final summary

## Components

- `src/main.py`: orchestrates scan flow
- `src/argParser.py`: validates CLI flags and converts scanType/hostid
- `src/networkScanner.py`: discovery, scanning, traceroute, storage
- `src/selfScan.py`: Linux `/proc` parsing for local listening sockets
- `src/generateReport.py`: boxed stdout reporting
- `src/traceNode.py`: traceroute node/path utilities

## Limitations

- Linux-only Self Scan (`/proc`)
- Root privileges usually required (raw packets)
- ICMP-heavy features may fail on networks that filter ICMP
- OS fingerprinting is heuristic and can be inaccurate behind NAT/firewalls
