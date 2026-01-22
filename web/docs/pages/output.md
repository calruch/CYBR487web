# Output & Reports

Output is printed to STDOUT using `src/generateReport.py`.

## What you’ll see

- A **Scan Starting** banner (network, ports, timeout)
- Per-host “Host Scan” summary blocks
- Optional port scan output (open ports)
- Optional traceroute output
- A final **Network Scan Summary** (hosts found, active hosts, start/end timestamps)

Verbose mode (`--verbose`) prints extra status messages (phase-by-phase).
