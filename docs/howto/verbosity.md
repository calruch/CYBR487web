# How-to: Increase verbosity

The CLI exposes two verbosity flags:

- `-v / --verbose` — prints status lines as the scan runs
- `-vv / --moreverbose` — parsed by the argument parser, but not currently used to change output

Example:

```bash
sudo python3 -m src.main --network 192.168.1.0/29 --scanType all --ports 22,80 -v
```
