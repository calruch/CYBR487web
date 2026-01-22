# Tutorial: First Scan (walkthrough)

This walkthrough is written to help a grader (or new teammate) understand what the tool does **without reading code**.

## Goal

Scan a small subnet, identify active hosts, detect OS category, check a few ports, and (optionally) traceroute.

## Step 1 — Pick a safe target

Choose a network you control. Example:

- Home lab: `192.168.1.0/24`
- VM-only test net: `10.0.2.0/24`

## Step 2 — Run a simple scan

```bash
sudo python3 main.py -n 192.168.1.0/24 --scanType all -p 22 80 443 -v
```

What this does (based on the current implementation):

1. Prints **Scan Starting**
2. Runs **Self Scan** by default when `--scanType all` (see note below)
3. Discovers hosts (ARP or ICMP host identification depending on `--hostid`)
4. For each discovered host:
   - optional OS fingerprint (ICMP-based)
   - optional TCP SYN port scan
   - optional traceroute
   - stores host info in memory and prints a host summary

!!! note "Why does Self Scan run when scanType=all?"
    In the current code, `scanType=all` and `scanType=SelfScan` both trigger the Self Scan step.
    This is documented behavior of the current snapshot. If you later change this behavior, update this page.

## Step 3 — Interpret results

- **Host Scan Result** shows MAC, OS category, whether host was marked active, and timestamp.
- The program also stores ports + traceroute results per host in a results structure (see **Output reference**).

If you don’t see expected hosts, see **Troubleshooting**.
