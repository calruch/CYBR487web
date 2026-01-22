# How-to: Scan a subnet

## Example

Scan a small subnet with the full scan mode:

```bash
sudo python3 -m src.main \
  --network 10.0.0.0/28 \
  --ports 22,80,443 \
  --scanType all \
  -v
```

## Tips

- Prefer small CIDRs for demos (`/29`, `/28`, `/27`).
- Host discovery method is controlled by `--hostid`:
  - `--hostid ARP` (default; best for local LANs)
  - `--hostid ICMP` (ping sweep)
  - `--hostid NONE` (skip discovery; useful for traceroute-only modes)
