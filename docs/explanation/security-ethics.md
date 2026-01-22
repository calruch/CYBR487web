# Security & ethics

This project is a network scanning tool. Network scanning can be intrusive and, in some contexts, illegal.

## Rules of thumb

- Only scan networks you own or have explicit authorization to test.
- Prefer small scopes for demos (e.g., a VM host-only network).
- Avoid scanning public IPs unless you have written permission.

## Safety considerations

- Use conservative timeouts and port ranges on production networks.
- Expect some environments to block ICMP or TCP probes.
