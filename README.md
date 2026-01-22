# MkDocs Material docs (GitHub Pages)

This folder set is designed to be copied into the **root** of your main project repo (same level as `src/`).

## Local preview

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r docs/requirements.txt
mkdocs serve
```

## GitHub Pages deployment (Actions)

1. Commit and push these files to your default branch (typically `main`).
2. In GitHub: **Settings → Pages**
3. Under **Build and deployment → Source**, choose **GitHub Actions**.
4. Push a new commit (or re-run the workflow) and check **Actions** tab.
5. Your site will be published at:
   - `https://<user>.github.io/<repo>/`

If your default branch is not `main`, update `.github/workflows/pages.yml`.
