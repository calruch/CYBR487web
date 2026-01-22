# Traceroute

Traceroute is implemented in `src/networkScanner.py` → `TraceRouteScanner`.

Two modes:

- ICMP traceroute (`--scanType=TraceRouteICMP` or `all`)
- TCP traceroute (`--scanType=TraceRouteTCP` or `all`)

The max hop count is controlled by `--maxhops` (default: 30, valid range: 1–60).
