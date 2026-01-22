from __future__ import annotations

from pathlib import Path
import mkdocs_gen_files

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src"

def is_public_module(path: Path) -> bool:
    name = path.name
    return (
        name.endswith(".py")
        and not name.startswith("_")
        and name not in {"__init__.py"}
    )

def main() -> None:
    # If src/ isn't present (e.g., someone opened only the docs skeleton),
    # generate a friendly placeholder so the build still succeeds.
    if not SRC.exists():
        with mkdocs_gen_files.open("reference/api/README.md", "w") as f:
            f.write(
                "# API reference generation\n\n"
                "No `src/` directory was found at build time.\n\n"
                "Unzip this docs folder into the project repo root (where `src/` exists), "
                "or update `scripts/gen_api_pages.py` to point to the correct code folder.\n"
            )
        return

    # Generate one page per module file.
    for py in sorted(SRC.rglob("*.py")):
        if not is_public_module(py):
            continue

        rel = py.relative_to(SRC).with_suffix("")
        mod = "src." + ".".join(rel.parts)

        doc_path = Path("reference/api") / ("/".join(rel.parts) + ".md")
        with mkdocs_gen_files.open(doc_path, "w") as f:
            title = mod
            f.write(f"# `{title}`\n\n")
            f.write("::: " + mod + "\n")

    # Generate an index listing.
    with mkdocs_gen_files.open("reference/api/index.md", "w") as f:
        f.write("# API reference\n\n")
        f.write("This section is generated from `src/` automatically.\n\n")
        f.write("## Modules\n\n")
        for py in sorted(SRC.rglob("*.py")):
            if not is_public_module(py):
                continue
            rel = py.relative_to(SRC).with_suffix("")
            page = "/".join(rel.parts) + ".md"
            mod = "src." + ".".join(rel.parts)
            f.write(f"- [{mod}]({page})\n")

if __name__ == "__main__":
    main()
