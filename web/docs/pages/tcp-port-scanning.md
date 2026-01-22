# TCP Port Scanning

TCP port scanning uses TCP SYN probes via Scapy:

- Send `SYN`
- If `SYN-ACK` is returned, the port is treated as open (and an RST is sent)
- If `RST-ACK` is returned, the port is closed
- If no response, the port is treated as filtered/unreachable

This behavior is implemented in `src/networkScanner.py` → `TCPPortScanner`.

> The TCP scan requires `--ports`. If the port list is missing or invalid, the scanner raises an error.
