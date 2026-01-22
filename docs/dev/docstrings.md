# Docstring guidance

The codebase uses docstrings extensively. To keep them consistent and useful, prefer **short, descriptive docstrings** that focus on:

- What the function/class does
- Parameters (names + types when non-obvious)
- Return value (type + meaning)
- Exceptions (when relevant)

## Recommended format

Use a lightweight Google-style format:

```python
def parse_ports(spec: str) -> list[int]:
    """Parse a port specification into a list of integers.

    Args:
        spec: Port spec string (e.g., "22", "22,80", "1-1024").

    Returns:
        A list of port integers.

    Raises:
        RuntimeError: If the input is syntactically invalid.
    """
    ...
```

## Practical rules

- Keep the first line as an imperative summary.
- Avoid repeating information that is obvious from the name.
- If a function is a public entrypoint, include examples.
- If behavior is heuristic or best-effort (e.g., OS fingerprinting), say so.

## Notes about the current code

Several modules use a `name:` / `description:` style in docstrings. That is acceptable, but if you refactor, consider migrating toward a single consistent style like the example above.
