# Scan Types

`--scanType` selects which phases run.

- `all` (default)  
  Runs:
  1) Self Scan
  2) Host discovery (ARP/ICMP)
  3) OS fingerprinting (ICMP IPID behavior)
  4) TCP port scanning (**requires `--ports`**)
  5) TCP traceroute
  6) ICMP traceroute

- `ICMP`  
  Host discovery + OS fingerprinting.

- `TCP`  
  Host discovery + TCP port scan (**requires `--ports`**).

- `TraceRouteTCP`  
  Host discovery + TCP traceroute.

- `TraceRouteICMP`  
  Host discovery + ICMP traceroute.

- `SelfScan`  
  Only Self Scan, then exits. `--network` is not required.
