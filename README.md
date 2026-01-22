# MkDocs Material documentation (CYBR487 Project 1)

This folder set provides a **MkDocs Material** documentation site that preserves the project's
black/white/red branding (EWU red accent) and includes automation for API docs.

## Where to place these files

Copy these files into the **root of your project repo** (same level as `src/`):

- `mkdocs.yml`
- `requirements.txt`
- `docs/`
- `scripts/`
- `.github/workflows/pages.yml` (optional, for GitHub Pages)

## Local preview

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
mkdocs serve
```

## Build (CI or local)

```bash
mkdocs build --strict
```

## GitHub Pages deployment

This repo includes a workflow at `.github/workflows/pages.yml` that builds and deploys
to GitHub Pages using the recommended **upload-pages-artifact** + **deploy-pages** actions.

### Required GitHub settings

In the GitHub repo:

1. Go to **Settings → Pages**
2. Under **Build and deployment**, set:
   - **Source**: *GitHub Actions*

After that, pushing to `main` will deploy.

## Branding notes

- Black background, white text, EWU red accent are implemented via:
  - `docs/stylesheets/extra.css`
- EWU logo white-outline effect is replicated via `filter: drop-shadow(...)` in that CSS.

## Placeholders you may need to fill

This documentation avoids guessing. Search for `Placeholder:` in the docs and update as needed
if your repo differs from the provided snapshots.
