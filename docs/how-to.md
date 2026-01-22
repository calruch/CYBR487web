# How-to guides

Task-focused recipes for common scanning goals.

!!! warning "Authorization required"
    Only scan networks and systems you own or have explicit permission to test.

## Scan a subnet

Use a CIDR network as the `--network` value. By default, host discovery uses **ARP**, which works best on the local L2 network.

```bash
sudo python3 -m src.main \
  --network=192.168.1.0/24 \
  --hostid=ARP \
  --ports=22,80,443 \
  --timeout=5 \
  --scanType=all \
  -v
```

### Prefer ICMP host discovery for routed networks

ARP discovery generally does not work across routers. If you are scanning a network that is not your local L2 segment, use ICMP host discovery:

```bash
sudo python3 -m src.main \
  --network=10.0.0.0/24 \
  --hostid=ICMP \
  --scanType=ICMP \
  --timeout=5 \
  -v
```

## Scan specific ports

`--ports` is a single string that supports:

- `22` (single port)
- `22,80,443` (comma-separated list)
- `1-1024` (inclusive range)

Spaces are not supported inside the port string.

Port scan only:

```bash
sudo python3 -m src.main \
  --network=192.168.1.0/24 \
  --hostid=ARP \
  --ports=1-1024 \
  --scanType=TCP \
  --timeout=5 \
  -v
```

## Run traceroute

There are two common ways to run traceroute.

### Traceroute as part of a scan

Use `--scanType=TraceRouteTCP` or `--scanType=TraceRouteICMP` with a host discovery method:

```bash
sudo python3 -m src.main \
  --network=192.168.1.0/24 \
  --hostid=ARP \
  --scanType=TraceRouteTCP \
  --maxhops=30 \
  --timeout=5 \
  -v
```

### Traceroute-only (skip host discovery)

Use `--hostid=NONE` to run traceroute directly against the provided target.

```bash
sudo python3 -m src.main \
  --network=192.168.1.1/32 \
  --hostid=NONE \
  --scanType=TraceRouteICMP \
  --maxhops=30 \
  --timeout=5 \
  -v
```

## Increase verbosity

- `-v` / `--verbose` enables additional status output and enables Scapy verbosity in some scanner components.
- `-vv` / `--moreverbose` is parsed but currently unused.

## Tune timeout and hop limit

- Use `--timeout=<seconds>` to control how long the tool waits for network responses (default is 5 seconds).
- Use `--maxhops=<int>` to cap traceroute hops (default is 30).

```bash
sudo python3 -m src.main \
  --network=192.168.1.0/24 \
  --hostid=ARP \
  --ports=22,80,443 \
  --scanType=all \
  --timeout=10 \
  --maxhops=20 \
  -v
```
