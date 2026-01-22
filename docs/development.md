# Development

This page is for contributors who want to understand or extend the codebase.

## Project layout (core modules)

The runtime entrypoint is `src.main`.

Key modules:

- `src/argParser.py`: CLI argument parsing and validation.
- `src/networkScanner.py`: scanning implementations (ARP/ICMP discovery, OS heuristic, TCP port scanning, traceroute).
- `src/selfScan.py`: local socket/process inspection via Linux `/proc`.
- `src/generateReport.py`: formatting and printing scan results.

## Running from source

From the repository root:

```bash
python3 -m src.main --scanType=SelfScan
```

## Extending the scanner

Common extension points:

- Add new scan modes to `src/main.py` and expose them via `--scanType` in `src/argParser.py`.
- Add new scanner classes/functions in `src/networkScanner.py`.
- Keep output consistent by using `src/generateReport.py` helpers.

## Documentation standards

- Keep CLI examples consistent with the actual CLI flags.
- Avoid duplicating the same information across multiple pages.
- Prefer short, task-focused sections and link to deeper reference when needed.

### Docstrings

Docstrings in this repository follow a structured, tool-friendly pattern:

- A brief description of the function/class purpose
- Parameters (types and meaning)
- Return value

When changing behavior, update both docstrings and public documentation to match.
