# Design & limitations

## Design goals

- Keep the tool approachable and readable for a class project
- Use widely-known techniques (ARP discovery, SYN scanning, traceroute)
- Provide a clean CLI and human-readable output

## Known limitations (based on snapshot behavior)

- **Linux bias**: Self Scan uses `/proc`
- **Privileges**: raw packet operations may require root/admin
- **Output completeness**: ports + traceroute are stored but not printed per host (easy fix)
- **OS fingerprint granularity**: OS detection is coarse and heuristic

## Suggested “teacher-friendly” improvements (optional)

If you want the documentation to be sufficient without code inspection, consider adding:

- Per-host printing of:
  - open ports
  - traceroute hops
- A `--json` option to export `results` to a file
- A `--no-self-scan` option (if you decide `all` should not trigger Self Scan)
