# How-to guides

Task-focused recipes for common scanning goals.

!!! warning "Authorization required"
    Only scan networks and systems you own or have explicit permission to test.

!!! note "If you used the Quick Start venv"
    Replace `python3` with `.venv/bin/python`. For privileged scans, prefer `sudo .venv/bin/python ...` so Scapy runs with the same interpreter you installed dependencies into.

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
  --network=10.0.0.0/24 \    # Change to desired network IP
  --hostid=ICMP \
  --scanType=OS \
  --timeout=5
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
  --scanType=PS \
  --timeout=5
```

## Run traceroute

There are two common ways to run traceroute.

### Traceroute as part of a scan

Use `--scanType=TRTCP` or `--scanType=TRICMP` with a host discovery method:

```bash
sudo python3 -m src.main \
  --network=192.168.1.0/24 \
  --hostid=ARP \
  --scanType=TRTCP \
  --maxhops=30 \
  --timeout=5
```

### Traceroute-only (skip host discovery)

Use `--hostid=NONE` to run traceroute directly against the provided target.

```bash
sudo python3 -m src.main \
  --network=192.168.1.1/32 \
  --hostid=NONE \
  --scanType=TRICMP \
  --maxhops=30 \
  --timeout=5
```

## Exclude targets with a whitelist file

Use `--file=<path>` to skip IPs/CIDRs. The file is whitespace-separated, for example:

```text
192.168.1.10
192.168.1.20/30
10.0.0.0/24
```

**Example**
```bash
sudo python3 -m src.main \
  --network=192.168.1.0/24 \
  --hostid=ARP \
  --ports=22,80,443 \
  --scanType=all \
  --file=whitelist.txt


## Increase verbosity

- `--verbose` enables additional status output and enables Scapy verbosity in some scanner components.
- `--moreverbose` enables additional debug-style output and increases Scapy verbosity in some scanner components.


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
```
