# Developer guide

## Project layout (expected)

Your project repo is expected to include:

- `src/` — Python modules (scanner components)
- `main.py` or `src/main.py` — entrypoint
- `docs/` — this documentation site (MkDocs)

If your live repo differs, update the paths in **Quick Start** and the `mkdocs.yml` `edit_uri`.

## Modules (from snapshot)

- `src/argParser.py` — CLI parsing and validation
- `src/networkScanner.py` — host discovery, OS detection, port scanning, traceroute, storage
- `src/generateReport.py` — boxed output formatting
- `src/selfScan.py` — local `/proc` socket scan
- `src/traceNode.py` — traceroute path/node utilities (used for organizing paths)
- `src/main.py` or `main.py` — scan orchestration

## Adding features (recommended approach)

1. Add logic to the relevant module in `src/`
2. Update CLI flags (if needed) in `src/argParser.py`
3. Update output formatting in `src/generateReport.py`
4. Update docs:
   - Add/update a How-to page
   - Update CLI reference
   - (If needed) update API reference stubs

## Running locally (development)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
mkdocs serve
```

Then open the local server URL printed by MkDocs.
