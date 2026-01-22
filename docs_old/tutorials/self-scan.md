# Tutorial: Self Scan (local ports)

Self Scan inspects local `/proc` socket data and associates ports with processes.

```bash
sudo python3 main.py --scanType SelfScan
```

!!! note "Linux-only"
    This feature depends on `/proc` and will not work on Windows.
