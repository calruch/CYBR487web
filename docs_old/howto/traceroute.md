# How-to: Run traceroute

ICMP traceroute:

```bash
sudo python3 main.py -n 192.168.1.0/24 --scanType TraceRouteICMP -m 30 -v
```

TCP traceroute:

```bash
sudo python3 main.py -n 192.168.1.0/24 --scanType TraceRouteTCP -m 30 -v
```
