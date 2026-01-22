# Docstring guide (MkDocs + mkdocstrings)

MkDocs Material can render API docs directly from Python docstrings via **mkdocstrings**.

## Recommended style

MkDocstrings parses several styles well. For VS Code + Python, **Google-style** docstrings are a good balance:

```python
def parse_network(value: str) -> list[str]:
    """Expand and validate a CIDR network.

    Args:
        value: CIDR string like "192.168.1.0/24".

    Returns:
        A list of IP strings in the target range.

    Raises:
        ValueError: If the network is invalid.
    """
```

!!! note "Current snapshot docstrings"
    The snapshot docstrings are valid Python docstrings, but they are more like a custom field format
    (`name: ...`, `description: ...`). Mkdocstrings will still render them as text, but you get better
    formatting if you convert to Google-style.

## VS Code extension to generate docstrings

Recommended extension:

- **autoDocstring** (`njpwerner.autodocstring`)

It can generate Google-style docstrings automatically.

Tip: In VS Code, open Command Palette → “Generate Docstring”.
