# CLI Options

These flags are parsed in `src/argParser.py` and consumed in `src/main.py`.

## Common flags

- `--network <IP/CIDR>`  
  Target IP or CIDR (example: `--network=192.168.1.0/24`).  
  **Required** unless `--scanType=SelfScan`.

- `--timeout <seconds>`  
  Timeout per probe in seconds. Defaults to `2`. Out-of-range or invalid values fall back to default.

- `--ports <ports>`  
  Ports to scan. Supported formats:
  - Range: `1-1023`
  - Comma list: `22,80,443`
  - Single: `80`

  > Required when the scan includes TCP port scanning (`--scanType=TCP` or `--scanType=all`).

- `-v, --verbose`  
  Enables status output.

- `-vv, --moreverbose`  
  Parsed, but currently not used for additional output in the core scan flow.

## Scan control

- `--hostid <ARP|ICMP>`  
  Selects host discovery method. Default is `ARP`.

- `--scanType <all|ICMP|TCP|TraceRouteTCP|TraceRouteICMP|SelfScan>`  
  Selects which scan phases run. Default is `all`.

- `-m, --maxhops <1-60>`  
  Max hop count for traceroute. Default is `30`.

## About `--help`

The argument parser disables argparse's built-in help (`add_help=False`) and treats `--help` as a boolean flag.  
At the moment, the application does not print usage output when `--help` is set.
