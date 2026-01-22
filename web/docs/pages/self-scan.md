# Self Scan

Self Scan reports local processes that have listening network sockets.

Implementation: `src/selfScan.py`

How it works:

1) Enumerate process file descriptors under `/proc/<pid>/fd`
2) Map socket inodes to entries in `/proc/net/tcp` and `/proc/net/udp`
3) Report processes in a listening-like state

Run it via:

```bash
sudo python3 -m src.main --scanType SelfScan --verbose
```
