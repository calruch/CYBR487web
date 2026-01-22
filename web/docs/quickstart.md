# Quick Start

This guide gets you from a fresh clone to a successful run without reading code.

## 1) Create and activate a virtual environment

From the repository root:

```bash
python3 -m venv env
source env/bin/activate
```

## 2) Install runtime dependencies

The application dependencies live in `misc/requirements.txt`.

```bash
pip install -r misc/requirements.txt
```

## 3) Run the tool

### Option A — automated script

The repo includes a convenience script:

```bash
chmod +x runApplication.sh
sudo ./runApplication.sh <IP_OR_CIDR>
```

What it does (currently): creates/activates a venv, installs `misc/requirements.txt`, then runs `python3 -m src.main` with a fixed port list and `--timeout=5 --verbose`.

### Option B — run directly

Scan a network (requires `--network`; ports are required for `all` and `TCP` scans):

```bash
sudo python3 -m src.main \
  --network=192.168.0.0/24 \
  --scanType=all \
  --ports=22,80,443 \
  --timeout=5 \
  --verbose
```

Run Self Scan only (no `--network` required):

```bash
sudo python3 -m src.main --scanType=SelfScan --verbose
```

## 4) (Optional) Run the unit tests

```bash
chmod +x runTest.sh
./runTest.sh
```

## Notes

- If you run without `sudo`, some scans may silently return less data (raw packets and `/proc/<pid>/fd` access often require elevated permissions).
- If `--scanType` is `all`, the program performs **both** traceroute variants (TCP and ICMP) for each discovered host.
