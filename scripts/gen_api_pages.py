\
from __future__ import annotations

from pathlib import Path
import mkdocs_gen_files

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src"

def is_public_module(path: Path) -> bool:
    return path.suffix == ".py" and not path.name.startswith("_") and path.name != "__init__.py"

def main() -> None:
    # If someone runs this docs skeleton outside the project repo, don't fail the build.
    if not SRC.exists():
        with mkdocs_gen_files.open("reference/api/index.md", "w") as f:
            f.write("# API reference\n\n")
            f.write("`src/` was not found at build time.\n\n")
            f.write("Unzip/copy these docs into the project repo root (where `src/` exists).\n")
        return

    # If src is a *regular* package, prefer documenting as src.<module>
    # Otherwise document modules directly (argParser, networkScanner, ...)
    prefix = "src." if (SRC / "__init__.py").exists() else ""

    modules = []
    for py in sorted(SRC.rglob("*.py")):
        if not is_public_module(py):
            continue

        rel = py.relative_to(SRC).with_suffix("")
        mod = prefix + ".".join(rel.parts)
        modules.append((mod, rel))

        doc_path = Path("reference/api") / ("/".join(rel.parts) + ".md")
        with mkdocs_gen_files.open(doc_path, "w") as f:
            f.write(f"# `{mod}`\n\n")
            f.write(f"::: {mod}\n")

    with mkdocs_gen_files.open("reference/api/index.md", "w") as f:
        f.write("# API reference\n\n")
        f.write("This section is generated automatically from the project's `src/` directory.\n\n")
        if not modules:
            f.write("No public modules were found under `src/`.\n")
            return
        f.write("## Modules\n\n")
        for mod, rel in modules:
            page = "/".join(rel.parts) + ".md"
            f.write(f"- [{mod}]({page})\n")

if __name__ == "__main__":
    main()
