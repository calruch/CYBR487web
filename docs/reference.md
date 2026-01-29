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

| Flag | Required | Default | Notes |
|---|---:|---:|---|
| `--network=<IPv4[/CIDR]>` | Yes (except `--scanType=SS`) | — | If no CIDR is provided, `/32` is assumed. |
| `-t/--timeout=<seconds>` | No | `2` | Valid range: `1–300`. Controls packet response wait time. |
| `-p/--ports=<ports>` | Yes for `all` and `PS` | — | Supports `22`, `22,80,443`, `1-1024` (inclusive). Spaces are not supported. |
| `-v/--verbose` | No | Off | Extra status output. |
| `-vv/--moreverbose` | No | Off | Enables verbose status output and increases Scapy verbosity for some operations. |
| `--scanType=<type>` | No | `all` | One of: `all`, `OS`, `PS`, `TRTCP`, `TRICMP`, `SS`. |
| `-s/--hostid=<ARP\|ICMP\|NONE>` | No | `ARP` | `NONE` is only valid with traceroute-only (`TRTCP`/`TRICMP`). |
| `-m/--maxhops=<int>` | No | `30` | Valid range: `1–60`. Traceroute hop limit. |
| `--file=<path>` | No | — | Whitelist/exclusion file: whitespace-separated IPs and/or CIDRs. Matching targets are skipped. |
| `--workers=<int>` | No | `1` | **WIP: Non-functional** Valid range: `1–64`. Uses multiprocessing to scan multiple hosts concurrently. |
| `-h/--help` | No | Off | Currently parsed but does not print a help screen (use docs as reference). |

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

- **Worker multiprocessing is malfunctioning**. It may crash or ruin scanner results if more than 1 worker is specified.
- **ARP host discovery is local-only**. ARP discovery generally does not work across routers/VLAN boundaries.
- **TCP traceroute uses destination port 80**. Some networks/firewalls may block or rate-limit this path.
- **ICMP traceroute printing may fail on timeouts**. Some timeout hops are recorded differently, which can cause traceroute printing to error when mixed with successful hops.
- **No file export**. Output is printed; no JSON/CSV writer is implemented.

## Common errors

### `No valid IPs were retrieved`

Cause: `--network` missing/invalid (and `--scanType` is not `SelfScan`).

Fix: provide a valid IPv4 address or CIDR, for example:

```bash
python3 -m src.main --network=192.168.1.0/24 --scanType=ICMP
```

### `Invalid host identifier was given`

Cause: `--hostid` must be `ARP`, `ICMP`, or `NONE` (case-sensitive).


### `Invalid scan type was given`

Cause: `--scanType` must be one of: `all`, `OS`, `PS`, `TRTCP`, `TRICMP`, `SS`.

