# OS Fingerprinting

The OS “fingerprinting” implemented here is **heuristic**. It sends ICMP packets and examines the IPID behavior.

The output categories are:

- Windows or FreeBSD
- Linux
- MacOS or IOS
- Unknown OS

See `src/networkScanner.py` → `ICMPHostIdentifier`.
