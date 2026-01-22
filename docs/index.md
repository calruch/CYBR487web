# Network Analyzer

Network Analyzer is a Linux-focused Python tool for **local socket inspection** and **basic network reconnaissance**.

!!! warning "Authorization required"
    Only scan networks and systems you own or have explicit permission to test.

## What it does

- **Self Scan (local)**: correlates listening TCP/UDP sockets with owning processes via Linux `/proc`.
- **Host discovery**: ARP (local L2 network) or ICMP (ping sweep).
- **OS family inference**: best-effort ICMP/IPID heuristic that categorizes a host as **Windows/FreeBSD**, **Linux**, **macOS/iOS**, or **Unknown**.
- **TCP SYN port scan**: scans a user-supplied set of TCP ports.
- **Traceroute**: ICMP traceroute or TCP traceroute (SYN to destination port 80) with a configurable hop limit.

## What it does not do

- It does **not** provide a stable public Python API.
- It does **not** export results to a file format (reporting is printed to STDOUT).
- `--help` is parsed but does **not** print usage/help output.

## Where to start

1. [Quickstart](quickstart.md)
2. [Tutorials](tutorials.md)
3. [How-to guides](how-to.md)
4. [Reference](reference.md)
5. [Concepts](concepts.md)
6. [Development](development.md)
