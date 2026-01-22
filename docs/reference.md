# Reference

This page describes the supported CLI interface and the tool's output format.

## Entrypoint

Run the scanner as a module:

```bash
python3 -m src.main [options]
```

!!! note "No interactive help"
    `-h/--help` is parsed, but it does not print usage/help output.

## Command-line options

| Option | Required? | Default | Notes |
|---|---:|---:|---|
| `--network=<IPv4[/CIDR]>` | Yes (except `SelfScan`) | — | If no CIDR is provided, `/32` is assumed. Invalid values fail argument processing. |
| `--ports=<spec>` | For `all` and `TCP` | — | Port specification must be a single string; see [Port specification](#port-specification). |
| `--timeout=<seconds>` | No | `5` | Clamped/validated to an integer range (1–10). Out-of-range values fall back to default. |
| `--scanType=<type>` | No | `all` | One of: `all`, `ICMP`, `TCP`, `TraceRouteTCP`, `TraceRouteICMP`, `SelfScan`. |
| `--hostid=<type>` | No | `ARP` | One of: `ARP`, `ICMP`, `NONE`. `NONE` skips discovery and supports traceroute-only mode. |
| `-m, --maxhops=<int>` | No | `30` | Traceroute hop limit (validated to 1–60). |
| `-v, --verbose` | No | `false` | Enables additional status output and enables Scapy verbosity in some scanner components. |
| `-vv, --moreverbose` | No | `false` | Parsed but currently unused. |
| `-h, --help` | No | `false` | Parsed but currently does not display help text. |

### Port specification

`--ports` supports these formats:

- `22` (single port)
- `22,80,443` (comma-separated list)
- `1-1024` (inclusive range)

Spaces are not supported inside the port string.

## Output format

The tool prints a series of boxed sections to STDOUT.

Typical `all` scan output includes:

- **Scan Starting**: echoes the selected network, ports, and timeout.
- **Self Scan Results**: printed first during `all` scans.
- **Host Scan (i/N)**: one per discovered host.
- **Port Scan**: open TCP ports for that host (when enabled).
- **Traceroute Results**: traceroute hops (when enabled).
- **Network Scan Summary**: totals at the end of the scan.

## Known limitations and gotchas

- **`--scanType=all` requires `--ports`**. If omitted, the TCP port scanner raises an error.
- **ARP host discovery is local-only**. ARP discovery generally does not work across routers/VLAN boundaries.
- **TCP traceroute uses destination port 80**. Some networks/firewalls may block or rate-limit this path.
- **ICMP traceroute printing may fail on timeouts**. Some timeout hops are recorded differently, which can cause traceroute printing to error when mixed with successful hops.
- **Self Scan can collapse duplicates**. If multiple processes share the same name, only one entry may be retained in the current output map.
- **No file export**. Output is printed; no JSON/CSV writer is implemented.

## Common errors

### `No valid IPs were retrieved`

Cause: `--network` missing/invalid (and `--scanType` is not `SelfScan`).

Fix: provide a valid IPv4 address or CIDR, for example:

```bash
python3 -m src.main --network=192.168.1.0/24 --scanType=ICMP
```

### `No ports given to scan`

Cause: `--scanType` includes TCP port scanning (`all` or `TCP`) but `--ports` was omitted.

Fix: supply ports:

```bash
python3 -m src.main --network=192.168.1.0/24 --ports=22,80,443 --scanType=TCP
```

### `Invalid host identifier was given`

Cause: `--hostid` must be `ARP`, `ICMP`, or `NONE` (case-sensitive).


### `Invalid scan type was given`

Cause: `--scanType` must be one of: `all`, `ICMP`, `TCP`, `TraceRouteTCP`, `TraceRouteICMP`, `SelfScan`.

