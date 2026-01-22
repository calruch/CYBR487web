# How-to: Scan a subnet

## Example

```bash
sudo python3 main.py -n 10.0.0.0/24 --scanType all -p 22 80 443 -v
```

## Tips

- Prefer a smaller subnet for demos: `/29`, `/28`, `/27`
- If host discovery misses devices, try switching host discovery method:
  - `--hostid ARP` (default in the snapshot)
  - `--hostid ICMP`

See **CLI reference** for exact flag details.
