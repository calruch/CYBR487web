# How-to: Scan a subnet

```bash
sudo python3 main.py -n 10.0.0.0/24 --scanType all -p 22 80 443 -v
```

Tips:
- Use small subnets for demos (e.g., `/28`)
- If ICMP is blocked, try ARP discovery on local LANs
