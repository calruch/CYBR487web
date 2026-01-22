# Output reference

This page explains what the tool prints **and** the in-memory result structure the program builds.

## Printed sections (current snapshot)

### Scan Starting

Printed at the beginning:

- Network
- Ports
- Timeout

### Host Scan Result

Printed per host:

- MAC
- OS (coarse category)
- Active flag
- Time

### Network Scan Summary

Printed at the end:

- Network
- Timeout
- Ports
- Hosts found
- Active hosts
- Started
- Ended

!!! note "Ports + traceroute visibility"
    The current `print_host_report()` output does **not** print ports or traceroute details, even though
    they are stored per host. If your teacher expects to see them in the report output, you may want to
    extend the report formatting (recommended improvement).

## Results structure

At the end of the scan, `main.py` builds:

```python
results = {
  "info": {
    "network": ipList,
    "ports": portList,
    "timeout": timeout,
    "started": started,
    "ended": ended,
  },
  "hosts": storage.getList(),
}
```

Each entry in `hosts` (from `HostStorage.addToList`) has the shape:

```python
{
  "IP": "<ip>",
  "MAC": "<mac or None>",
  "HostInfo": {
    "OS": "<string>",
    "active": <bool>,
    "Time": "<datetime>",
    "Ports": <list or None>,
    "TraceRoute": <list/dict or None>
  }
}
```

## OS categories

The HostStorage translation function maps:

- `1` → "Windows or FreeBSD"
- `2` → "Linux"
- `3` → "MacOS or IOS"
- `4` → "Unknown OS"
- `5` → "Inactive Host"
