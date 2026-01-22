# Quick Start

## Requirements

From the repository README:

- Linux-based OS required
- Python **3.12+**
- Bash is required for the helper scripts
- WSL *may* work, but is not guaranteed

## 1) Install requirements (manual)

From the project repo root:

```bash
python3 -m venv env
source env/bin/activate
pip install -r misc/requirements.txt
```

> Many scan features use raw packets (Scapy). On most systems you will need to run scans with `sudo`.

## 2) Run a scan (recommended)

Use the provided script:

```bash
chmod +x runApplication.sh
sudo ./runApplication.sh <IP-or-CIDR>
```

Example:

```bash
sudo ./runApplication.sh 192.168.0.0/24
```

### What the script does

`runApplication.sh` currently:

- Creates a venv named `env`
- Installs `misc/requirements.txt`
- Runs:

```bash
python3 -m src.main --network=<CIDR> --timeout=5 --verbose --ports=4682,6969,8000,544,8096,8080,8443,8888,9000,9090,9200,9300,11211,27017
```

If you want a different timeout/port set, edit `runApplication.sh`.

## 3) Run manually

```bash
source env/bin/activate
sudo python3 -m src.main --network=192.168.0.0/24 --timeout=5 --verbose --ports=22,80,443
deactivate
```

## 4) Self Scan (no `--network` required)

```bash
sudo python3 -m src.main --scanType SelfScan --verbose
```

Self Scan reads `/proc` and reports listening sockets by process name.
