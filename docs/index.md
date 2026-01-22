# Network Analyzer Documentation

Network Analyzer is a Linux-focused Python tool for local socket inspection and basic network reconnaissance.

## Capabilities

- **Self Scan (local)**: correlate TCP/UDP sockets with owning processes via Linux `/proc`.
- **Host discovery**: ARP (local network) or ICMP (ping sweep).
- **OS family inference**: best-effort ICMP/IPID-based categorization (Windows/FreeBSD, Linux, macOS/iOS, Unknown).
- **TCP SYN port scan**: scan a user-supplied set of TCP ports.
- **Traceroute**: ICMP traceroute or TCP traceroute (SYN to destination port 80) with configurable hop limit.

!!! warning "Authorization required"
    Only scan networks and systems you own or have explicit permission to test.

## Where to start

- **Quick Start**: install + run commands and a “known-good” first scan.
- **Tutorials**: step-by-step walkthroughs for common tasks (subnet scan, port scan, traceroute, Self Scan).
- **Reference**: flags and output notes.
