# Documentation (MkDocs Material)

This folder contains the documentation site.

## Local preview

From the repo root:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r web/requirements.txt
mkdocs serve -f web/mkdocs.yml
```

## Build

```bash
mkdocs build --strict -f web/mkdocs.yml
```

## Notes on API reference

The API reference pages are generated from `src/` at build time.

For best results, make sure `src/` is importable. The minimal (recommended) approach is to add:

- `src/__init__.py`
