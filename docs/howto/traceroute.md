# How-to: Run traceroute

Traceroute supports two modes:

- `TraceRouteICMP` (ICMP-based traceroute)
- `TraceRouteTCP` (TCP-based traceroute; SYN to destination port 80)

## ICMP traceroute

```bash
sudo python3 -m src.main --network 192.168.1.0/29 --scanType TraceRouteICMP -m 30 -v
```

## TCP traceroute

```bash
sudo python3 -m src.main --network 192.168.1.0/29 --scanType TraceRouteTCP -m 30 -v
```

## Host discovery interaction

By default, traceroute runs against the hosts returned by the selected discovery method (`--hostid ARP` or `--hostid ICMP`).

If you want traceroute-only behavior across the entire target CIDR without discovery, use:

```bash
sudo python3 -m src.main --network 192.168.1.0/29 --hostid NONE --scanType TraceRouteICMP -m 30 -v
```

!!! warning "`--hostid NONE` + `--scanType all`"
    When host discovery is disabled, the current implementation returns early for most scan types. Use the dedicated traceroute scan types (`TraceRouteICMP` / `TraceRouteTCP`) with `--hostid NONE`.

## Max hops

Use `-m/--maxhops` to adjust hop limit. The parser enforces **1–60**.
