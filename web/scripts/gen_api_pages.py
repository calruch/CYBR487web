from __future__ import annotations

from pathlib import Path
import mkdocs_gen_files

# This script lives at: web/scripts/gen_api_pages.py
# We want the project root (one level above /web)
PROJECT_ROOT = Path(__file__).resolve().parents[2]
SRC_DIR = PROJECT_ROOT / "src"

API_ROOT = Path("reference/api")
INDEX_PATH = API_ROOT / "index.md"

def iter_modules(src_dir: Path):
    for path in sorted(src_dir.glob("*.py")):
        if path.name.startswith("_"):
            continue
        yield path

with mkdocs_gen_files.open(INDEX_PATH, "w") as f:
    f.write("# API Reference\n\n")
    f.write("This section is generated automatically from the Python modules in `src/`.\n\n")
    f.write("## Modules\n\n")

    if not SRC_DIR.exists():
        f.write("> **Note:** `src/` was not found at build time. Run this documentation inside the project repo root.\n")
    else:
        for mod_path in iter_modules(SRC_DIR):
            mod_name = mod_path.stem
            page = API_ROOT / f"{mod_name}.md"
            with mkdocs_gen_files.open(page, "w") as pf:
                pf.write(f"# `{mod_name}`\n\n")
                pf.write(f"::: src.{mod_name}\n")
            f.write(f"- [`{mod_name}`]({mod_name}.md)\n")
