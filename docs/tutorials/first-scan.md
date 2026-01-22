# Tutorial: First Scan (walkthrough)

This walkthrough demonstrates a small, permissioned scan and explains how to interpret the output.

## Goal

- Discover hosts on a small network
- Infer an OS family category (best-effort)
- Scan a short list of TCP ports
- Run traceroute (ICMP + TCP) as part of an “all” scan

## Step 1 — Pick a safe target

Choose a network you control. Examples:

- Home network: `192.168.1.0/29` or `192.168.1.0/28`
- VM-only test net: `10.0.2.0/28`

## Step 2 — Run the scan

`--scanType all` runs **Self Scan**, host discovery, OS inference, TCP port scanning, and both traceroute variants.

```bash
sudo python3 -m src.main \
  --network 192.168.1.0/29 \
  --ports 22,80,443 \
  --scanType all \
  -v
```

!!! note "Why does Self Scan run when scanType=all?"
    In the current implementation, `--scanType all` triggers the Self Scan step before scanning remote hosts.

## Step 3 — Interpret results

- **Scan Starting**: echoes the network, ports, and timeout.
- **Self Scan Results**: local TCP/UDP sockets associated to processes (Linux `/proc`).
- **Host Scan: (i/N)**: per-host summary (IP, MAC if known, OS family string, active flag, timestamp).
- **Port Scan:**: open TCP ports found on each host (only when port scanning is enabled).
- **Traceroute Results**: hop-by-hop output for traceroute (only when traceroute is enabled).
- **Network Scan Summary**: end-of-run counts and timestamps.

If you don’t see expected hosts:

- Try `--hostid ICMP` to switch discovery method, or reduce the target to a smaller CIDR.
- Ensure you have the required privileges for raw packet operations.
