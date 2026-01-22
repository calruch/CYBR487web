# Troubleshooting

## `PermissionError` / raw socket errors

Many scan types require raw packets and may require root:

```bash
sudo python3 main.py ...
```

## No hosts discovered

Try:

- Ensure you're scanning the correct interface/network
- Use ICMP host discovery:

```bash
sudo python3 main.py -n 192.168.1.0/24 --hostid ICMP --scanType ICMP -v
```

- If ICMP is blocked on the network, use ARP discovery on a local subnet.

## Running inside a VM

VM networking mode matters:

- NAT may block inbound probes
- Bridged mode tends to work better for LAN scans
- Host-only networks are excellent for safe demos

## Slow scans / timeouts

- Reduce the number of ports
- Reduce subnet size
- Increase timeout slightly (`-t 3`, `-t 5`)

## Known limitations

- Self Scan depends on `/proc` (Linux-only)
- OS fingerprinting is heuristic (may be wrong behind NAT/firewalls)

If something is missing here, add it as soon as you discover it.
