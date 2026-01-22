# Troubleshooting

## Pages deploy shows 404

Confirm:
- GitHub repo **Settings → Pages → Source: GitHub Actions**
- An Actions run completed successfully
- You are visiting the correct URL:
  - `https://<user>.github.io/<repo>/`

## API reference is empty

- Confirm your project repo has `src/` at the root.
- If mkdocstrings can’t resolve modules, add `src/__init__.py` (recommended) or ensure modules are discoverable.

## Build fails on GitHub Actions

Open the Actions log and look for the first error:
- Missing dependency (install it in `docs/requirements.txt`)
- Broken Markdown link (fix the link or file name)
