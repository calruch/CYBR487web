# Quick Start

This page covers the minimum steps to install and run the tool.

## 1) Prerequisites

- **Linux recommended** (Self Scan relies on `/proc`)
- **Python 3.10+**
- **Privileges**: ARP/ICMP/SYN scanning and traceroute typically require root or `CAP_NET_RAW`

!!! note "Scapy dependency"
    The scanner uses Scapy for packet crafting and sending. If raw packet features fail, try running with `sudo` (or grant `CAP_NET_RAW` to your Python interpreter).

## 2) Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## 3) Install dependencies

```bash
pip install -r requirements.txt
```

## 4) Run a first scan

> The entrypoint imports from a package named `src` (e.g., `from src.argParser import ...`). If your checkout has a `src/` directory, use the command below. If not, align your directory layout to match those imports before running.

```bash
sudo python3 -m src.main \
  --network 192.168.1.0/29 \
  --ports 22,80,443 \
  --scanType all \
  -v
```

## 5) Confirm output

You should see boxed sections such as:

- **Scan Starting**
- **Self Scan Results** (runs as part of `--scanType all`)
- **Host Scan: (i/N)** for discovered hosts
- **Network Scan Summary**
