# Usage

## Scan types (practical examples)

### Full scan

Runs self-scan, discovery, OS detect, TCP scan, and traceroute:

```bash
sudo python3 -m src.main --network=192.168.0.0/24 --scanType=all --hostid=ARP --timeout=2 --ports=22,80,443 -v
```

### Self Scan only (no network required)

```bash
sudo python3 -m src.main --scanType=SelfScan -v
```

### ICMP discovery + OS detect

```bash
sudo python3 -m src.main --network=192.168.0.0/24 --scanType=ICMP --hostid=ICMP -v
```

### TCP scan only (ports required)

```bash
sudo python3 -m src.main --network=192.168.0.0/24 --scanType=TCP --ports=1-1023 -v
```

### Traceroute only

```bash
sudo python3 -m src.main --network=192.168.0.0/24 --scanType=TraceRouteTCP --maxhops=30 -v
sudo python3 -m src.main --network=192.168.0.0/24 --scanType=TraceRouteICMP --maxhops=30 -v
```

## Common troubleshooting

- If discovery finds zero hosts, try switching `--hostid` between `ARP` and `ICMP`.
- If scans error with permission problems, run with `sudo`.
- If ICMP is filtered on the network, ICMP discovery/OS detection may not work.
