# Network Analyzer

A Linux-first network analysis tool that combines:

- **Host discovery** via ARP or ICMP ping
- **OS fingerprinting** via ICMP responses
- **TCP SYN port scanning**
- **Traceroute** (TCP and ICMP)
- **Self Scan** to list local TCP/UDP sockets by process (from `/proc`)

!!! warning "Authorization"
    Only scan networks and systems you own or have explicit permission to test.

## Quick start

If you already have the repo checked out, start here:

- **Quick Start** → installation + the fastest working commands
- **CLI** → exact flags and valid values (matches `src/argParser.py`)
- **How It Works** → what each scan mode does and how modules fit together

## Requirements (runtime)

- Linux (Self Scan reads `/proc`, and Scapy is used for packet operations)
- Python 3.12+ (per README)
- Root/admin privileges are commonly required for ARP, TCP SYN scanning, and traceroute

