# How-to: Scan specific ports

Single port:

```bash
sudo python3 main.py -n 192.168.1.0/24 --scanType TCP -p 22
```

Multiple ports:

```bash
sudo python3 main.py -n 192.168.1.0/24 --scanType TCP -p 22 80 443
```

Range:

```bash
sudo python3 main.py -n 192.168.1.0/24 --scanType TCP -p 1-1023
```
