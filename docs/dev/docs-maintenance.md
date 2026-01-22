# Documentation maintenance

This repository’s documentation is maintained as Markdown files.

## What to keep in sync

When code changes, update the relevant docs:

- **CLI changes** (`argParser.py`) → update **cli.md** and **README.md** examples
- **Scan pipeline changes** (`main.py`, `networkScanner.py`, `selfScan.py`) → update **how-it-works.md** and **design-limitations.md**
- **Output formatting changes** (`generateReport.py`) → update **output.md**

## Documentation quality checklist

Before merging documentation updates:

- No non-technical references or personal identifiers
- All commands and flags match the current parser
- Examples use supported `--ports` formats (single, comma list, or range)
- Notes about privileges and platform requirements are accurate
- Headings, code blocks, and lists render cleanly in Markdown

## Suggested workflow

1. Make the code change.
2. Update the relevant Markdown file(s).
3. Run a quick sanity pass:
   - `python3 -m unittest discover -s . -p "test*.py"` (if tests are present and passing)
   - Run one representative scan command (in an authorized environment).
