# Quick Start (the teacher-friendly version)

This is the **minimum** set of steps to install and run a scan without digging through code.

## 1) Prerequisites

- **Linux** (the project uses `/proc` for Self Scan and raw packet features via Scapy)
- **Python 3.10+** recommended
- Admin/root privileges are often required for raw packet operations (e.g., SYN scan, ARP)

!!! note "Scapy dependency"
    The project uses `scapy` (and therefore your OS may need packet capture capabilities).
    If Scapy is installed but raw packets fail, see **Troubleshooting**.

## 2) Create a virtual environment (recommended)

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## 3) Install dependencies

If your project repo already includes a requirements file, use it.

If you **do not** have one yet, minimum needed (per code imports) is:

```bash
pip install scapy
```

## 4) Run a first scan

### Option A — `main.py` is at the repo root

```bash
sudo python3 main.py -n 192.168.1.0/24 --scanType all -p 22 80 443 -v
```

### Option B — `main.py` is inside `src/`

```bash
sudo python3 src/main.py -n 192.168.1.0/24 --scanType all -p 22 80 443 -v
```

If neither is true, update the entrypoint path above to match your repo.

## 5) Confirm the output

The program prints boxed sections like:

- **Scan Starting**
- **Scanning (i/N): \<IP\>**
- **Host Scan Result: \<IP\>**
- **Network Scan Summary**

See **Reference → Output reference** for the full data layout.
