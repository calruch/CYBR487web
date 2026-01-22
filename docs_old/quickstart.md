# Quick Start

This is the fastest path to running a scan **without reading code**.

## Prerequisites

- Linux
- Python 3.10+ recommended
- Root/admin may be required for raw packet operations

## Install docs toolchain (local preview)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r docs/requirements.txt
```

## Run a first scan

Update the entrypoint path below to match your repo (common options shown):

```bash
sudo python3 main.py -n 192.168.1.0/24 --scanType all -p 22 80 443 -v
```

or

```bash
sudo python3 src/main.py -n 192.168.1.0/24 --scanType all -p 22 80 443 -v
```

!!! note "Placeholder: entrypoint"
    If neither `main.py` nor `src/main.py` exists in your repo, replace the command above with the correct entrypoint.
