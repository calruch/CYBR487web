# Tutorial: Self Scan (local sockets)

Self Scan inspects Linux `/proc` to associate sockets with processes, then prints a boxed summary.

## Run Self Scan only

```bash
sudo python3 -m src.main --scanType SelfScan -v
```

`--network` is not required for `SelfScan`.

## What you should see

A box titled **Self Scan Results** containing lines like:

- Process name
- Protocol (`tcp` / `udp`)
- Local address and port
- Remote address and port

!!! note "Output nuance"
    The current implementation returns one socket entry per process name (later matches can overwrite earlier ones). Treat the output as a lightweight summary rather than a complete per-process socket list.

!!! note "Linux-only"
    This feature depends on `/proc` and is not expected to work on non-Linux systems.
