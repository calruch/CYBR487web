# Troubleshooting

## `RuntimeError: No valid IPs were retrieved`

- Your `--network` value was missing or invalid **and** the scan type was not `SelfScan`.
- Use a valid IP or CIDR like `192.168.0.0/24`.

## `RuntimeError: No valid ports were given.`

- You ran a scan that includes TCP port scanning (`all` or `TCP`) without a valid `--ports` list.
- Example: `--ports=22,80,443` or `--ports=1-1023`.

## Permission / Scapy errors

- Scapy-based scans often require elevated privileges.
- Try running with `sudo`.

## Self Scan shows nothing

- The Self Scan filter focuses on listening-like socket states.
- If you want “all connections,” you may need to adjust the filter in `src/selfScan.py`.
