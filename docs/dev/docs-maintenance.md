# Docs maintenance

## Local preview

From the project repo root:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
mkdocs serve
```

## Build for CI

```bash
mkdocs build --strict
```

## API reference automation

This site includes a script that generates API reference markdown pages from your `src/` folder:

- `scripts/gen_api_pages.py` runs during the MkDocs build (via `mkdocs-gen-files`).

If your `src/` path changes, update:

- `mkdocs.yml` → `plugins.mkdocstrings.handlers.python.paths`
- `scripts/gen_api_pages.py` source root
