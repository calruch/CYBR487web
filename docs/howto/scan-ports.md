# How-to: Scan specific ports

Port scanning uses TCP SYN probes and requires `--ports`.

!!! note "Required flag"
    `--ports` must be provided for `--scanType TCP` and `--scanType all`. The current implementation raises an error if no valid ports are supplied.

## Single port

```bash
sudo python3 -m src.main --network 192.168.1.0/29 --scanType TCP --ports 22 -v
```

## Comma-separated list

```bash
sudo python3 -m src.main --network 192.168.1.0/29 --scanType TCP --ports 22,80,443 -v
```

## Range

```bash
sudo python3 -m src.main --network 192.168.1.0/29 --scanType TCP --ports 1-1023 -v
```

!!! note "Performance"
    Large ranges (for example `1-65535`) can take a long time and may require increasing `--timeout`.
