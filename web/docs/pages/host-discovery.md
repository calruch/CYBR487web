# Host Discovery

Host discovery is selected with `--hostid`.

## ARP (default)

ARP discovery sends ARP requests for the target network and records `(IP, MAC)` pairs.

## ICMP

ICMP discovery expands the CIDR into individual hosts and sends ICMP Echo Requests.
Hosts that respond are recorded as `(IP, None)` because ICMP discovery does not learn MAC addresses.
