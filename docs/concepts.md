# Concepts

This section explains how the tool works at a high level, along with design limitations and safe-use guidance.

## High-level workflow

At runtime, the scanner follows this sequence:

1. Parse CLI arguments.
2. Print a **Scan Starting** header (network, ports, timeout).
3. If `--scanType` is `all` or `SS`, run **Self Scan** first.
4. If host discovery is enabled (`--hostid=ARP` or `--hostid=ICMP`), build a list of target hosts.
5. For each discovered host, run the selected scan modules (OS heuristic, port scan, traceroute) based on `--scanType`.
6. Print per-host reports and a final **Network Scan Summary**.

## Scan types and discovery modes

### `--hostid`

- `ARP`: ARP discovery on the local L2 segment.
- `ICMP`: ICMP echo sweep across the provided CIDR.
- `NONE`: skip discovery.

### `--scanType`

- `all`: runs Self Scan, OS heuristic, TCP port scan, and both traceroute modes.
- `ICMP`: OS heuristic only (requires host discovery).
- `TCP`: TCP port scan only (requires `--ports`).
- `TRTCP`: TCP traceroute (requires host discovery unless used with `--hostid=NONE`).
- `TRICMP`: ICMP traceroute (requires host discovery unless used with `--hostid=NONE`).
- `SS`: local-only self scan.

!!! note "Traceroute-only mode"
    When `--hostid=NONE`, the tool only runs traceroute for `TraceRouteTCP` and `TraceRouteICMP`, then exits early.

## OS family inference (ICMP/IPID heuristic)

The OS inference is a **best-effort heuristic** based on changes in the IP identification (IPID) field between two ICMP responses.

- Small deltas (0–64) are categorized as **Windows/FreeBSD**
- Medium deltas (65–128) are categorized as **Linux**
- Larger deltas (>128) are categorized as **macOS/iOS**
- If responses are missing or the pattern doesn’t match, the result is **Unknown**

This is not a fingerprinting engine; NAT devices, load balancers, kernel settings, and network conditions can skew results.

## Design limitations

- **ARP discovery is local-only**: it generally won’t discover hosts across routers.
- **ICMP discovery can be blocked**: some hosts and networks drop ICMP echo requests.
- **TCP port scanning is SYN-only**: it checks for SYN-ACK replies and sends an RST to close.
- **No UDP port scanning**: the tool does not implement UDP service discovery.
- **TCP traceroute uses destination port 80**: middleboxes may treat this differently from ICMP.
- **Output is STDOUT-only**: there is no built-in JSON/CSV writer.

## Security and ethics

- Get explicit authorization before scanning.
- Scope narrowly: start with small CIDR blocks and a minimal port list.
- Expect detection: scans can trigger IDS/IPS alerts and rate limits.
- Minimize impact: use reasonable timeouts and avoid large ranges on production networks.
- Handle results responsibly: scan outputs can contain sensitive information (host/IP inventory and open ports).
