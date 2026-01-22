# Network Scanner Documentation

This project is a Python-based network scanning tool that can:

- Discover hosts on a target IPv4 network (ARP on local L2, or ICMP echo across a CIDR range)
- Heuristically fingerprint a host OS family using ICMP/IPID behavior
- Perform a TCP SYN port scan against a list/range of ports
- Run TCP- or ICMP-based traceroute
- Run a local “self scan” by correlating `/proc` sockets with `/proc/net` entries (Linux)

## Quick start

> Many features use raw packets and typically require elevated privileges.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Typical scan (host discovery + OS heuristic + SYN scan + traceroute)
sudo python3 -m src.main --network=192.168.1.0/24 --hostid=ARP --ports=22,80,443 --timeout=5 --scanType=all -v

# Local self scan (no --network required)
sudo python3 -m src.main --scanType=SelfScan
```

If your checkout does not provide a `src/` package, see **Developer guide** for layout expectations.

## Documentation map

- **README.md** — high-level overview and setup
- **cli.md** — complete CLI reference (flags, required inputs, examples)
- **how-it-works.md** — code-grounded explanation of the scan pipeline
- **output.md** — what the tool prints and how results are structured in memory
- **troubleshooting.md** — common errors and fixes
- **design-limitations.md** — known limitations and practical constraints
- **security-ethics.md** — safety and authorization guidance
- **developer-guide.md** — development notes, tests, and repository layout
- **docstrings.md** — docstring style guidance
- **docs-maintenance.md** — how to keep the Markdown docs accurate over time
