# Usage

## Common patterns

### Full scan (`all`, default)

> Requires `--ports` because it includes TCP port scanning.

```bash
sudo python3 -m src.main --network=192.168.0.0/24 --ports=22,80,443 --verbose
```

### ICMP-only scan (no ports required)

```bash
sudo python3 -m src.main --network=192.168.0.0/24 --scanType=ICMP --verbose
```

### TCP-only scan

```bash
sudo python3 -m src.main --network=192.168.0.0/24 --scanType=TCP --ports=1-1023 --verbose
```

### Traceroute-only scans

```bash
sudo python3 -m src.main --network=192.168.0.0/24 --scanType=TraceRouteTCP --maxhops=30 --verbose
sudo python3 -m src.main --network=192.168.0.0/24 --scanType=TraceRouteICMP --maxhops=30 --verbose
```

### Self Scan (local only)

```bash
sudo python3 -m src.main --scanType=SelfScan --verbose
```

## Notes

- `--network` is required for every scan type **except** `SelfScan`.
- If the scan includes TCP port scanning (`all` or `TCP`), you **must** provide `--ports`.
