# Developer guide

This guide is for developers working on the scanner codebase.

## Repository layout (expected by the current code)

The Python imports and scripts reference a `src/` package:

- `python3 -m src.main`
- `from src.argParser import ParseClass`

If your checkout currently has the Python files at the repository root, align the layout by placing them under `src/` (or adjust `PYTHONPATH` accordingly).

Key modules:

- `argParser.py` — argument parsing and validation
- `networkScanner.py` — ARP/ICMP discovery, OS heuristic, SYN scan, traceroute
- `selfScan.py` — `/proc` correlation (Linux)
- `generateReport.py` — console formatting
- `main.py` — orchestrates the run and returns the results dict

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Notes:

- The code uses `match/case` (Python 3.10+).
- Scapy typically requires elevated privileges for raw packets.

## Running

See **cli.md** for the full reference.

Example:

```bash
sudo python3 -m src.main --network=192.168.1.0/24 --hostid=ARP --ports=22,80,443 --scanType=all -v
```

## Tests

This repository includes unit tests such as `testArg.py`, `testScanner.py`, and `testReport.py`.

A generic way to run all tests (without relying on a `tst/` directory) is:

```bash
python3 -m unittest discover -s . -p "test*.py"
```

## Contributing expectations

- Keep CLI behavior consistent with `ParseClass.buildParser()`.
- When changing scan behavior or output formatting, update **cli.md**, **how-it-works.md**, and **output.md**.
- Prefer small, testable functions for scanner behavior.
