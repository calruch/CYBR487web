# How-to: Run traceroute

Traceroute can be run in two modes:

- `TraceRouteICMP` (ICMP-based traceroute)
- `TraceRouteTCP` (TCP-based traceroute)

## ICMP traceroute

```bash
sudo python3 main.py -n 192.168.1.0/24 --scanType TraceRouteICMP -m 30 -v
```

## TCP traceroute

```bash
sudo python3 main.py -n 192.168.1.0/24 --scanType TraceRouteTCP -m 30 -v
```

## Max hops

Use `-m/--maxhops` to adjust hop limit. The parser enforces 1–60.
