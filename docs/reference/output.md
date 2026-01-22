# Output and results

This tool prints **formatted console output** and also builds an in-memory results dictionary.

> The current code does **not** write JSON or files to disk.

## Console output

Output is produced by `generateReport.py`.

### Scan start

At the beginning of a run, the tool prints a boxed header:

- Network (the CIDR string you provided)
- Ports (only if `--ports` was provided; printed as the Python list)
- Timeout

### Self scan results

When `--scanType=all` or `--scanType=SelfScan`, a “Self Scan Results” section is printed with entries like:

- Process name
- Protocol (`tcp` or `udp`)
- Local address (`ip:port`)
- Remote address (`ip:port`)

Notes:

- Only TCP state `0A` (LISTEN) and UDP state `07` are included.
- The current implementation shows at most one connection per process name.

### Host scan results

For each discovered host, the tool prints a “Host Scan” section that includes:

- IP
- MAC (for ARP-discovered hosts; `None` for ICMP-discovered hosts)
- OS (heuristic string)
- Active (boolean)
- Time (timestamp at the moment the host record was stored)

### Port scan results

When `--scanType=all` or `--scanType=TCP`, the tool prints a “Port Scan” section per host:

- IP
- A list of open ports (`Port: <n>` per line)

Only open ports are printed.

### Traceroute results

When `--scanType=all` or a traceroute-only scan type is used, the tool may print traceroute results:

- Target IP
- Rows of `Hop: <n> | IP: <hop_ip or *> | Time: <ms>`

If a trace returns `None` (for example, first hops are timeouts), the tool prints a short note instead of a table.

### End-of-scan summary

At the end, a “Network Scan Summary” section is printed with:

- Network
- Timeout
- Hosts found
- Active hosts
- Started / Ended timestamps

## In-memory results structure

`main.py` builds and returns a dictionary in this shape:

```python
results = {
    "info": {
        "network": ipList,        # CIDR string
        "timeout": timeout,
        "started": started,       # datetime
        "ended": ended,           # datetime
    },
    "hosts": [
        {
            "IP": "192.168.1.10",
            "MAC": "aa:bb:cc:dd:ee:ff" or None,
            "HostInfo": {
                "OS": "Linux" | "Windows or FreeBSD" | "MacOS or IOS" | "Unknown OS" | "Inactive Host",
                "active": True | False,
                "Time": datetime,
                "Ports": [22, 80] or None,
                "TraceRouteTCP": list | None,
                "TraceRouteICMP": list | None,
            },
        },
        # ... more hosts
    ],
}
```

A few practical notes:

- `"Ports"` will be `None` unless a TCP scan was run.
- Traceroute lists are a sequence of `[hop, ip, rtt_ms]` entries (or `None`).
- OS strings are produced by `HostStorage._translateOStype()`.
