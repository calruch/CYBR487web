# Tutorial: First scan (walkthrough)

## Goal

Discover active hosts on a small subnet, collect OS hints, scan a few ports, and optionally run traceroute.

## Example command

```bash
sudo python3 main.py -n 192.168.1.0/24 --scanType all -p 22 80 443 -v
```

## What to look for

- A scan-start summary (network/ports/timeout)
- Per-host result blocks (MAC/OS/active/time)
- A final network summary

If results look wrong, see **Reference → Troubleshooting**.
