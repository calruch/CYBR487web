# How-to: Increase verbosity

The tool exposes two verbosity levels:

- `-v / --verbose` — standard status output
- `-vv / --moreverbose` — more detailed output (implementation-dependent)

Example:

```bash
sudo python3 main.py -n 192.168.1.0/24 --scanType all -p 22 80 -vv
```
