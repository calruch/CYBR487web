# Documentation site (MkDocs Material)

This folder contains the MkDocs project for the Network Analyzer documentation site.

## Preview locally

From the repo root:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r web/requirements-docs.txt
mkdocs serve -f web/mkdocs.yml
```

Then open the URL printed by MkDocs.

## Build

```bash
mkdocs build -f web/mkdocs.yml
```

> Note: The docs import the project modules (e.g. `src.main`) for the API Reference page.
> Build from a working checkout of the main repo so `src/` is present.
