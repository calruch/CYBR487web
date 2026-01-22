# Install & Run

## Requirements

- **Linux**: Self Scan reads `/proc` (Linux-only).
- **Python 3.x**
- **Privileges**: raw packet operations via Scapy typically require **root**.

## Install dependencies

From repository root:

```bash
python3 -m venv env
source env/bin/activate
pip install -r misc/requirements.txt
```

## Run

### Using the provided runner (recommended)

```bash
chmod +x runApplication.sh
sudo ./runApplication.sh 192.168.0.0/24
```

### Manual run

```bash
source env/bin/activate
sudo python3 -m src.main --network=192.168.0.0/24 --scanType=all --ports=80,443 -v
deactivate
```

## Notes

- `--network` is required for all modes **except** `--scanType=SelfScan`.
- `--ports` is required for TCP scanning modes (otherwise the TCP scanner errors).
