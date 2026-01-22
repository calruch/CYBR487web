# Security and ethics

This tool performs network probing (ARP, ICMP, TCP SYN) and traceroute operations.

## Authorized use only

- Only scan networks and hosts you **own** or have **explicit permission** to test.
- Make sure your activity complies with local laws, organizational policies, and acceptable-use rules.

## Operational safety

- Prefer the smallest possible scope (use narrow CIDR ranges and limited port lists).
- Use conservative timeouts and rate limits when scanning fragile networks.
- Expect that some environments will flag scanning activity (IDS/IPS, endpoint firewalls).

## Data handling

- The tool prints results to the console and holds results in memory.
- If you add persistent logging/export in the future, consider how you will protect:
  - Host identifiers (IPs/MACs)
  - Scan results (open ports, topology information)
  - Any associated timestamps

## Responsible disclosure

If you discover unexpected exposure or vulnerabilities while testing with permission:

- Follow your organization’s disclosure process.
- Share only the minimum details required to remediate.
