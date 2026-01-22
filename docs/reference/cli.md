# CLI reference

This page is derived from the current argument parser implementation (`src/argParser.py` in the snapshot).

## Synopsis

```bash
python3 main.py [OPTIONS]
```

## Options

| Flag | Meaning | Example |
|---|---|---|
| `-n`, `--network` | Target network in CIDR notation | `-n 192.168.1.0/24` |
| `-p`, `--ports` | Port list or range to scan | `-p 22 80 443` or `-p 1-1023` |
| `-t`, `--timeout` | Timeout (seconds) | `-t 2` |
| `-v`, `--verbose` | Verbose output | `-v` |
| `-vv`, `--moreverbose` | Extra verbose output | `-vv` |
| `-s`, `--hostid` | Host discovery method (`ARP` or `ICMP`) | `--hostid ICMP` |
| `-m`, `--maxhops` | Max hops for traceroute (1–60) | `-m 30` |
| `--scanType` | Scan mode selector (see below) | `--scanType TCP` |
| `-h`, `--help` | Print help | `-h` |

## `--scanType` values

The parser accepts these string values (case-sensitive in the snapshot):

- `all`
- `ICMP`
- `TCP`
- `TraceRouteTCP`
- `TraceRouteICMP`
- `SelfScan`

Internally, these map to numeric modes used by `main.py`.

!!! note "Case sensitivity"
    If your team changes the parser to accept lower/upper case variants, update this page accordingly.

## Ports input formats

Supported formats:

- Single port: `-p 22`
- Space-separated: `-p 22 80 443`
- Range: `-p 1-1023`

The parser validates ports in the range 1–65535.
