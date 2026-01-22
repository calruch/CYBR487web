# Command-line reference

## Entrypoint

The scanning CLI is implemented in `main.py` and expects to be invoked as the module `src.main`:

```bash
python3 -m src.main [OPTIONS]
```

> Note: in the current code, imports use `src.*`. If your repository layout does not include a `src/` package, you will need to run with an adjusted `PYTHONPATH` (or align the layout). See **developer-guide.md**.

## Options

All options below are **case-sensitive** where noted.

| Option | Required | Description |
|---|---:|---|
| `--network=<IPv4[/CIDR]>` | **Yes** (except `SelfScan`) | Target network in CIDR notation. If no CIDR is provided, `/32` is assumed. Example: `--network=192.168.1.0/24` or `--network=192.168.1.10` |
| `--ports=<spec>` | Required for `--scanType=all` or `--scanType=TCP` | Ports to scan. See **Port specification** below. |
| `--timeout=<seconds>` | No | Timeout for most network operations. Must be an integer `1–300`. Invalid/out-of-range values fall back to the default (`5`). |
| `--hostid=ARP|ICMP|NONE` | No | Host discovery mode. Default: `ARP`. `NONE` skips host discovery and is intended for traceroute-only runs. |
| `--scanType=all|ICMP|TCP|TraceRouteTCP|TraceRouteICMP|SelfScan` | No | Scan mode selector. Default: `all`. |
| `-m, --maxhops=<int>` | No | Max hops for traceroute. Valid range: `1–60`. Default: `30`. |
| `-v, --verbose` | No | Enables additional status output and enables Scapy verbosity inside scan functions. |
| `-vv, --moreverbose` | No | Parsed but currently **unused** (reserved for future expansion). |
| `-h, --help` | No | Parsed but currently **does not print usage/help output**. Use this document for help. |

### Port specification (`--ports`)

`--ports` accepts a **single string** in one of these forms:

- **Single port:** `--ports=22`
- **Comma-separated list:** `--ports=22,80,443`
- **Range (inclusive):** `--ports=1-1023`

Spaces are **not** supported (for example, `--ports=22 80 443` will not parse correctly).

## Examples

Typical “all” scan (host discovery + OS heuristic + SYN scan + traceroute):

```bash
sudo python3 -m src.main --network=192.168.1.0/24 --hostid=ARP --ports=22,80,443 --timeout=5 --scanType=all -v
```

OS heuristic only (still performs host discovery based on `--hostid`):

```bash
sudo python3 -m src.main --network=192.168.1.0/24 --hostid=ICMP --scanType=ICMP -v
```

Port scan only (still performs host discovery based on `--hostid`):

```bash
sudo python3 -m src.main --network=192.168.1.0/24 --hostid=ARP --ports=1-1024 --scanType=TCP -v
```

Traceroute-only (recommended: target a single host with `/32`):

```bash
sudo python3 -m src.main --network=192.168.1.1/32 --hostid=NONE --maxhops=30 --scanType=TraceRouteTCP
```

Self scan (local machine):

```bash
sudo python3 -m src.main --scanType=SelfScan
```
