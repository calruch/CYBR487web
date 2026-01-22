# Tutorials

These walkthroughs show common end-to-end workflows using the CLI.

!!! warning "Authorization required"
    Only scan networks and systems you own or have explicit permission to test.

## Tutorial: First network scan (scanType = `all`)

This tutorial runs:

- Host discovery (ARP by default)
- OS heuristic (ICMP/IPID)
- TCP SYN port scan
- Traceroute (TCP + ICMP)

### 1) Pick a small target range

Start with a narrow CIDR (for example, a `/29`) so the output is easy to review.

### 2) Choose a port set

For `--scanType=all`, you must provide `--ports`.

Good starter list:

- `22` (SSH)
- `80` (HTTP)
- `443` (HTTPS)

### 3) Run the command

```bash
sudo python3 -m src.main \
  --network=192.168.1.0/29 \
  --hostid=ARP \
  --ports=22,80,443 \
  --timeout=5 \
  --scanType=all \
  -v
```

### 4) Read the output

You should see, in order:

- **Scan Starting**: echoes your selected network, ports, and timeout.
- **Self Scan Results**: printed first during `all` scans.
- A **Host Scan (i/N)** box per discovered host.
- **Port Scan** output per host (when `--scanType` includes TCP port scanning).
- **Traceroute Results** boxes (TCP and/or ICMP) when traceroute is enabled.
- **Network Scan Summary** at the end.

If no hosts are discovered, see [Troubleshooting and limitations](reference.md#known-limitations-and-gotchas).

## Tutorial: Local Self Scan (scanType = `SelfScan`)

Self Scan inspects your local machine's listening sockets and attempts to map them to process names.

```bash
sudo python3 -m src.main --scanType=SelfScan
```

### What to expect

- Output appears under **Self Scan Results**.
- Only sockets in a "listening" state are considered.
- Running without `sudo` can limit visibility into other users' processes.

!!! note "Current limitation"
    The Self Scan result map is keyed by process name. If multiple processes share the same name (for example, two `python3` servers on different ports), only one entry may be retained in the output.

## Tutorial: Traceroute-only (no host discovery)

Traceroute-only mode skips host discovery and runs traceroute directly against the provided target.

```bash
sudo python3 -m src.main \
  --network=192.168.1.1/32 \
  --hostid=NONE \
  --maxhops=30 \
  --scanType=TraceRouteTCP
```

Notes:

- Traceroute-only mode prints traceroute results, then exits (it does not print the final summary report).
- The target may be a CIDR. In that case, the tool expands the CIDR into individual hosts and traceroutes each one.
