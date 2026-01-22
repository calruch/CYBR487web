# How-to: Scan specific ports

The tool supports multiple port input formats.

## Single port

```bash
sudo python3 main.py -n 192.168.1.0/24 --scanType TCP -p 22 -v
```

## Space-separated ports

```bash
sudo python3 main.py -n 192.168.1.0/24 --scanType TCP -p 22 80 443
```

## Range

```bash
sudo python3 main.py -n 192.168.1.0/24 --scanType TCP -p 1-1023
```

!!! note "Performance"
    Large ranges (e.g., `1-65535`) will take longer and may cause timeouts depending on your network and timeout setting.
