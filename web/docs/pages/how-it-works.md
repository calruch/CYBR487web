# How It Works

The main entrypoint is `python3 -m src.main`.

High-level flow:

1) Parse CLI flags with `src/argParser.py`
2) Print scan-start banner via `src/generateReport.py`
3) If `scanType` is `all` or `SelfScan`, run `src/selfScan.py`
4) Discover hosts via ARP or ICMP (`src/networkScanner.py`)
5) For each host:
   - OS fingerprint (ICMP IPID behavior) when enabled
   - TCP port scan when enabled
   - TCP/ICMP traceroute when enabled
6) Print per-host results and a final summary
