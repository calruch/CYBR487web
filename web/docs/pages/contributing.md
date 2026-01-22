# Contributing

## Running the application

See **Quick Start**.

## Running tests

The provided script runs unit tests using `unittest` discovery:

```bash
chmod +x runTest.sh
./runTest.sh
```

Notes:

- `runTest.sh` expects an ASCII banner file at `misc/ascii/name.txt`.
- It runs `python3 -m unittest discover -s tst/` (so tests should live under `tst/`).

## Coding conventions

- Follow PEP 8 formatting guidelines.
- Write docstrings for classes and functions (aim for clear inputs/outputs).
