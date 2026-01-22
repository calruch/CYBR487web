# Troubleshooting

## “the following arguments are required: --network” / “No valid IPs were retrieved”

For scan types other than `SelfScan`, you must provide `--network`.

Example:

```bash
sudo python3 -m src.main --network=192.168.1.0/24 --hostid=ARP --scanType=ICMP -v
```

## Port scan runs but finds nothing

Make sure you supplied `--ports` in a supported format:

- `--ports=22`
- `--ports=22,80,443`
- `--ports=1-1024`

If you run `--scanType=all` or `--scanType=TCP` without `--ports`, the port scanner will raise an error.

## “PermissionError” / no results unless using sudo

Many operations use raw packets (Scapy) and typically require elevated privileges.

Try:

```bash
sudo python3 -m src.main --network=192.168.1.0/24 --hostid=ARP --ports=22,80,443 --scanType=all
```

For `SelfScan`, you may also need elevated privileges to read `/proc/<pid>/fd` entries for other processes.

## ARP discovery finds nothing

ARP discovery works only on the local L2 segment (same broadcast domain). If you are scanning a routed network or a VPN segment, try ICMP host discovery instead:

```bash
sudo python3 -m src.main --network=10.0.0.0/24 --hostid=ICMP --scanType=ICMP
```

## Traceroute prints “no results”

Traceroute results may be suppressed when early hops time out.

Things to try:

- Increase `--maxhops` (valid range `1–60`)
- Increase `--timeout` (valid range `1–300`)
- Prefer TCP traceroute (`--scanType=TraceRouteTCP`) if ICMP is blocked

Example:

```bash
sudo python3 -m src.main --network=192.168.1.1/32 --hostid=NONE --maxhops=30 --timeout=5 --scanType=TraceRouteTCP
```

## The `-h/--help` flag doesn’t show usage

The CLI currently parses `-h/--help` as a normal boolean flag, but no code prints argparse help/usage.

Use **cli.md** for the supported options and examples.

## Convenience scripts don’t work

`runApplication.sh` and `runTest.sh` reference paths like `misc/...` and `tst/...`. If your repository does not include those directories, run the commands directly (examples are in **README.md** and **cli.md**).
