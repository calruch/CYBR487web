# Tutorial: Self Scan (local ports)

Self Scan inspects `/proc` to associate open sockets with running processes, then prints a boxed summary.

## Run Self Scan only

```bash
sudo python3 main.py --scanType SelfScan
```

If your entrypoint is `src/main.py`, run that instead.

## What you should see

A box titled **Self Scan Results** containing lines like:

- Process name
- Protocol (tcp/udp)
- Local address + port
- Remote address + port

!!! note "Linux-only"
    This feature depends on `/proc` and is not expected to work on Windows.
