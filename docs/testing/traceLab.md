# 6-VM VirtualBox Routed Network Lab (Client → R1 → R2 → R3 → Server LANs)

<style>
  /* Offline-friendly styling for MkDocs HTML rendering */
  :root {
    --fg: #1a1a1a;
    --muted: #5a5a5a;
    --bg: #ffffff;
    --border: #d9d9d9;
    --tableHead: #f4f5f7;
    --codeBg: #f7f7f9;
  }

  .md-content, body {
    color: var(--fg);
    background: var(--bg);
    line-height: 1.55;
  }

  h1, h2, h3 {
    letter-spacing: 0.2px;
    margin-top: 1.2em;
  }

  p, li {
    max-width: 1100px;
  }

  .callout {
    border: 1px solid var(--border);
    border-left: 4px solid #4a7bd0;
    padding: 0.75rem 1rem;
    background: #fbfcff;
    margin: 1rem 0;
  }

  .muted {
    color: var(--muted);
  }

  table {
    border-collapse: collapse;
    width: 100%;
    margin: 0.75rem 0 1.25rem 0;
    font-size: 0.95rem;
  }

  th, td {
    border: 1px solid var(--border);
    padding: 0.55rem 0.6rem;
    vertical-align: top;
  }

  th {
    background: var(--tableHead);
    text-align: left;
    font-weight: 600;
  }

  code {
    background: var(--codeBg);
    padding: 0.1rem 0.25rem;
    border-radius: 4px;
  }

  pre {
    background: var(--codeBg);
    border: 1px solid var(--border);
    padding: 0.85rem 1rem;
    border-radius: 8px;
    overflow-x: auto;
    line-height: 1.35;
  }

  pre code {
    background: transparent;
    padding: 0;
  }

  .tight ul {
    margin-top: 0.25rem;
  }
</style>

## 1) Overview

This lab documents a 6-VM VirtualBox network that demonstrates basic multi-hop IPv4 routing across isolated L2 segments. A client system (ClientVM) resides on a host-only LAN and reaches two server LANs via a routed chain of three Linux router VMs (R1 → R2 → R3). Static routing is configured via Netplan on each router, with kernel forwarding enabled to permit transit traffic.

Key concepts demonstrated:

- Layer-3 routing across distinct L2 segments (host-only and internal networks)
- Point-to-point transit networks using /30 addressing between routers
- Static routes to provide end-to-end reachability without dynamic routing
- Validation using `ip route`, `ping`, and `traceroute`

## 2) Environment Summary

### VirtualBox segmentation model

- **Host-only network (VirtualBox):**
  - **Client LAN** uses **vboxnet1** (host-only).
  - Connected to **ClientVM** and **R1** (R1’s host-only interface).

- **Internal networks (VirtualBox):**
  - All non-client segments are **VirtualBox internal networks**:
    - Transit link between R1 and R2 (10.10.12.0/30)
    - Transit link between R2 and R3 (10.10.23.0/30)
    - Server LAN S2 (10.10.20.0/24)
    - Server LAN S3 (10.10.30.0/24)

<div class="callout">
  <strong>Note:</strong> Only <code>vboxnet1</code> is explicitly named. The VirtualBox internal network names (e.g., the configured names for net12/net23/S2/S3 in the VirtualBox UI) are not provided in the inputs and are documented in <em>Assumptions / Unknowns</em>.
</div>

## 3) Topology

<pre><code>┌──────────────────────────────────────────────────────────────────────────────┐
│ CLIENT LAN                                                                   │
│ 192.168.57.0/24                                                              │
│                                                                              │
│ Client VM                                                                    │
│ IP: 192.168.57.100/24                                                        │
│ Default GW: 192.168.57.254 (R1 on this LAN)                                  │
└───────────────────────────────────┬──────────────────────────────────────────┘
                                    │ (Host-only segment: vboxnet1)
                                    │
                                    │ R1 host-only interface:
                                    │ 192.168.57.254/24
                          ┌─────────┴──────────────────────────────────────────┐
                          │ R1                                                   │
                          │ Router 1 (edge)                                      │
                          │                                                      │
                          │ IF_hostonly: 192.168.57.254/24                       │
                          │ IF_net12: 10.10.12.1/30                              │
                          │ ip_forward=1                                         │
                          └─────────┬──────────────────────────────────────────┘
                                    │
                     Transit link "net12"
                     Network: 10.10.12.0/30
                     - usable: 10.10.12.1 (R1), 10.10.12.2 (R2)
                     - broadcast: 10.10.12.3
                                    │
                                    │ R2 net12 interface:
                                    │ 10.10.12.2/30
                          ┌─────────┴──────────────────────────────────────────┐
                          │ R2                                                   │
                          │ Router 2 (core)                                      │
                          │                                                      │
                          │ IF_net12: 10.10.12.2/30                              │
                          │ IF_net23: 10.10.23.1/30                              │
                          │ IF_netS2: 10.10.20.1/24 (Gateway for S2 LAN)         │
                          │ ip_forward=1                                         │
                          └─────────┬───────────────────────────┬──────────────┘
                                    │                           │
                                    │                           │
                 ┌──────────────────┘            └─────────────────────┐
                 │                                                     │
┌──────────────────────────────────────────────┐     ┌──────────────────────────────────────────────┐
│ SERVER LAN (S2)                               │     │ Transit link "net23"                         │
│ 10.10.20.0/24                                 │     │ Network: 10.10.23.0/30                        │
│                                               │     │ - usable: 10.10.23.1 (R2),                    │
│ serverr2 VM                                   │     │   10.10.23.2 (R3)                              │
│ IP: 10.10.20.100/24                           │     │ - broadcast: 10.10.23.3                        │
│ Default GW: 10.10.20.1 (R2 IF_netS2)          │     │                                                │
└──────────────────────────────────────────────┘     │ R3 net23 interface: 10.10.23.2/30            │
                                                     └──────────────────────────┬───────────────────┘
                                                                                │
                                                                     ┌─────────┴─────────────────────┐
                                                                     │ R3                              │
                                                                     │ Router 3 (edge)                 │
                                                                     │                                 │
                                                                     │ IF_net23: 10.10.23.2/30         │
                                                                     │ IF_netS3: 10.10.30.1/24         │
                                                                     │ (Gateway for S3 LAN)            │
                                                                     │ ip_forward=1                    │
                                                                     └─────────┬─────────────────────┘
                                                                                │
                                                        ┌─────────────────┴─────────────────────┐
                                                        │ SERVER LAN (S3)                        │
                                                        │ 10.10.30.0/24                           │
                                                        │                                         │
                                                        │ serverr3 VM                              │
                                                        │ IP: 10.10.30.100/24                      │
                                                        │ Default GW: 10.10.30.1 (R3 IF_netS3)     │
                                                        └───────────────────────────────────────┘</code></pre>

## 4) Addressing Plan

### Subnet: Client LAN

| CIDR | Purpose | VirtualBox adapter type | Connected interfaces | Default gateway behavior |
|---|---|---|---|---|
| 192.168.57.0/24 | Client LAN (host-only segment) | Host-only (**vboxnet1**) | ClientVM `enp0s3` (192.168.57.100/24), R1 `enp0s3` (192.168.57.254/24) | ClientVM default route via **192.168.57.254** (R1) |

### Subnet: Transit link R1 ↔ R2

| CIDR | Purpose | VirtualBox adapter type | Connected interfaces | Default gateway behavior |
|---|---|---|---|---|
| 10.10.12.0/30 | Point-to-point transit between R1 and R2 | Internal network | R1 `enp0s8` (10.10.12.1/30), R2 `enp0s3` (10.10.12.2/30) | No default gateways defined; static routes provide reachability between LANs |

### Subnet: Transit link R2 ↔ R3

| CIDR | Purpose | VirtualBox adapter type | Connected interfaces | Default gateway behavior |
|---|---|---|---|---|
| 10.10.23.0/30 | Point-to-point transit between R2 and R3 | Internal network | R2 `enp0s8` (10.10.23.1/30), R3 `enp0s3` (10.10.23.2/30) | No default gateways defined; static routes provide reachability between LANs |

### Subnet: Server LAN S2

| CIDR | Purpose | VirtualBox adapter type | Connected interfaces | Default gateway behavior |
|---|---|---|---|---|
| 10.10.20.0/24 | Server LAN S2 behind R2 | Internal network | R2 `enp0s9` (10.10.20.1/24), serverr2 `enp0s3` (10.10.20.100/24) | serverr2 default route via **10.10.20.1** (R2) |

### Subnet: Server LAN S3

| CIDR | Purpose | VirtualBox adapter type | Connected interfaces | Default gateway behavior |
|---|---|---|---|---|
| 10.10.30.0/24 | Server LAN S3 behind R3 | Internal network | R3 `enp0s8` (10.10.30.1/24), serverr3 `enp0s3` (10.10.30.100/24) | serverr3 default route via **10.10.30.1** (R3) |

## 5) VM Inventory (6 VMs)

### ClientVM

- **Role:** Client endpoint on Client LAN (host-only).
- **Interfaces:**
  - `enp0s3` → `192.168.57.100/24` → Client LAN (vboxnet1)
- **Default route:**
  - `default via 192.168.57.254`
- **Static routes:** None beyond default route.

### R1 (Router 1, edge to Client LAN)

- **Role:** Edge router between Client LAN and transit to R2.
- **Interfaces:**
  - `enp0s3` → `192.168.57.254/24` → Client LAN (vboxnet1)
  - `enp0s8` → `10.10.12.1/30` → Transit R1↔R2 (10.10.12.0/30)
- **Default route:** Not specified in Netplan artifacts.
- **Static routes (from Netplan):**
  - `10.10.20.0/24 via 10.10.12.2`
  - `10.10.30.0/24 via 10.10.12.2`
  - `10.10.23.0/30 via 10.10.12.2`

### R2 (Router 2, core)

- **Role:** Core router connecting transit links and Server LAN S2.
- **Interfaces:**
  - `enp0s3` → `10.10.12.2/30` → Transit R1↔R2 (10.10.12.0/30)
  - `enp0s8` → `10.10.23.1/30` → Transit R2↔R3 (10.10.23.0/30)
  - `enp0s9` → `10.10.20.1/24` → Server LAN S2 (10.10.20.0/24)
- **Default route:** Not specified in Netplan artifacts.
- **Static routes (from Netplan):**
  - `192.168.57.0/24 via 10.10.12.1`
  - `10.10.30.0/24 via 10.10.23.2`

### R3 (Router 3, edge to Server LAN S3)

- **Role:** Edge router between transit from R2 and Server LAN S3.
- **Interfaces:**
  - `enp0s3` → `10.10.23.2/30` → Transit R2↔R3 (10.10.23.0/30)
  - `enp0s8` → `10.10.30.1/24` → Server LAN S3 (10.10.30.0/24)
- **Default route:** Not specified in Netplan artifacts.
- **Static routes (from Netplan):**
  - `192.168.57.0/24 via 10.10.23.1`
  - `10.10.20.0/24 via 10.10.23.1`

### serverr2 (Server on S2 LAN)

- **Role:** Server endpoint on Server LAN S2.
- **Interfaces:**
  - `enp0s3` → `10.10.20.100/24` → Server LAN S2 (10.10.20.0/24)
- **Default route:**
  - `default via 10.10.20.1`
- **Static routes:** None beyond default route.

### serverr3 (Server on S3 LAN)

- **Role:** Server endpoint on Server LAN S3.
- **Interfaces:**
  - `enp0s3` → `10.10.30.100/24` → Server LAN S3 (10.10.30.0/24)
- **Default route:**
  - `default via 10.10.30.1`
- **Static routes:** None beyond default route.

## 6) Routing Design

### Linux forwarding requirement (R1/R2/R3)

R1, R2, and R3 function as transit routers and must forward IPv4 packets between interfaces. This requires enabling:

- `net.ipv4.ip_forward=1`

The provided `persistentRouting.sh` script enforces this at boot (via `/etc/sysctl.d/99-router.conf`) and applies the settings immediately using `sysctl --system`.

### Reverse path filtering configuration intent

The script also disables reverse path filtering:

- `net.ipv4.conf.all.rp_filter=0`
- `net.ipv4.conf.default.rp_filter=0`

**Configuration intent in this lab:** This setting reduces the chance that Linux will drop packets due to asymmetric routing checks during multi-interface routing scenarios. This is documented as the intent for this environment, not as a universal best practice.

### Static routing (authoritative from Netplan)

This lab uses static routes (no dynamic routing protocols). Each route below is taken directly from the authoritative Netplan artifacts.

#### R1 static routes (next hop: R2 at 10.10.12.2)

| Destination | Next hop | What it enables |
|---|---:|---|
| 10.10.20.0/24 | 10.10.12.2 | Client LAN ↔ Server LAN S2 reachability via R2 |
| 10.10.30.0/24 | 10.10.12.2 | Client LAN ↔ Server LAN S3 reachability via R2/R3 |
| 10.10.23.0/30 | 10.10.12.2 | Reachability to the R2↔R3 transit network from R1 |

#### R2 static routes (next hop: R1 at 10.10.12.1; R3 at 10.10.23.2)

| Destination | Next hop | What it enables |
|---|---:|---|
| 192.168.57.0/24 | 10.10.12.1 | Server LANs ↔ Client LAN return path via R1 |
| 10.10.30.0/24 | 10.10.23.2 | Server LAN S2 ↔ Server LAN S3 and Client LAN ↔ Server LAN S3 via R3 |

#### R3 static routes (next hop: R2 at 10.10.23.1)

| Destination | Next hop | What it enables |
|---|---:|---|
| 192.168.57.0/24 | 10.10.23.1 | Server LAN S3 ↔ Client LAN return path via R2/R1 |
| 10.10.20.0/24 | 10.10.23.1 | Server LAN S3 ↔ Server LAN S2 reachability via R2 |

## 7) Expected Traffic Flows (Hop-by-Hop)

This section describes the expected L3 hop sequence based on addressing and static routes.

### ClientVM → serverr2 (192.168.57.100 → 10.10.20.100)

**Expected path:**
1. **ClientVM** sends to default gateway **192.168.57.254** (R1 `enp0s3`)
2. **R1** forwards toward **10.10.20.0/24 via 10.10.12.2** (R2) over transit **10.10.12.0/30**
3. **R2** delivers to **10.10.20.100** over Server LAN S2 (R2 `enp0s9`)

**Expected router IP hops (typical traceroute):**
- Hop 1: 192.168.57.254 (R1)
- Hop 2: 10.10.12.2 (R2 transit-side interface toward R1)
- Hop 3: 10.10.20.100 (serverr2)

### ClientVM → serverr3 (192.168.57.100 → 10.10.30.100)

**Expected path:**
1. **ClientVM** sends to default gateway **192.168.57.254** (R1)
2. **R1** forwards toward **10.10.30.0/24 via 10.10.12.2** (R2)
3. **R2** forwards toward **10.10.30.0/24 via 10.10.23.2** (R3)
4. **R3** delivers to **10.10.30.100** over Server LAN S3 (R3 `enp0s8`)

**Expected router IP hops (typical traceroute):**
- Hop 1: 192.168.57.254 (R1)
- Hop 2: 10.10.12.2 (R2)
- Hop 3: 10.10.23.2 (R3 transit-side interface toward R2)
- Hop 4: 10.10.30.100 (serverr3)

### serverr2 ↔ serverr3 (10.10.20.100 ↔ 10.10.30.100)

**serverr2 → serverr3 expected path:**
1. **serverr2** sends to default gateway **10.10.20.1** (R2)
2. **R2** forwards toward **10.10.30.0/24 via 10.10.23.2** (R3)
3. **R3** delivers to **10.10.30.100** on Server LAN S3

**serverr3 → serverr2 expected path:**
1. **serverr3** sends to default gateway **10.10.30.1** (R3)
2. **R3** forwards toward **10.10.20.0/24 via 10.10.23.1** (R2)
3. **R2** delivers to **10.10.20.100** on Server LAN S2

**Expected router IP hops (typical traceroute):**
- serverr2 → serverr3:
  - Hop 1: 10.10.20.1 (R2)
  - Hop 2: 10.10.23.2 (R3)
  - Hop 3: 10.10.30.100 (serverr3)
- serverr3 → serverr2:
  - Hop 1: 10.10.30.1 (R3)
  - Hop 2: 10.10.23.1 (R2)
  - Hop 3: 10.10.20.100 (serverr2)

## 8) Validation Procedures

The following checks validate addressing, routing, and forwarding. Commands assume a Linux environment on each VM.

### Per VM: verify interface addressing and routes

Run on **each VM**:

```bash
ip a
ip route
```


## Expected highlights

### ClientVM
- `enp0s3` has `192.168.57.100/24`
- default route via `192.168.57.254`

### serverr2
- `enp0s3` has `10.10.20.100/24`
- default route via `10.10.20.1`

### serverr3
- `enp0s3` has `10.10.30.100/24`
- default route via `10.10.30.1`

### R1/R2/R3
- expected interface IPs per inventory
- expected static routes per Netplan

## Routers: verify forwarding and rp_filter settings

Run on R1, R2, and R3:

```bash
sysctl net.ipv4.ip_forward
sysctl net.ipv4.conf.all.rp_filter
sysctl net.ipv4.conf.default.rp_filter
ip route
```
## Expected outputs

- `net.ipv4.ip_forward = 1`
- `net.ipv4.conf.all.rp_filter = 0`
- `net.ipv4.conf.default.rp_filter = 0`
- Route table contains the static routes described in Section 6

## Segment connectivity tests (ping)

Run these as targeted validations:

### ClientVM
```bash
# Validate Client LAN and R1 reachability
ping -c 3 192.168.57.254

# Validate end-to-end reachability to server LANs
ping -c 3 10.10.20.100
ping -c 3 10.10.30.100

serverr2
# Validate local gateway
ping -c 3 10.10.20.1

# Validate reachability to serverr3 and back toward Client LAN
ping -c 3 10.10.30.100
ping -c 3 192.168.57.100

serverr3
# Validate local gateway
ping -c 3 10.10.30.1

# Validate reachability to serverr2 and back toward Client LAN
ping -c 3 10.10.20.100
ping -c 3 192.168.57.100

Path validation (traceroute)

Traceroute confirms hop-by-hop routing behavior. Use ICMP or UDP traceroute depending on installed tooling; the hop IPs should align with Section 7.

ClientVM
traceroute -n 10.10.20.100
traceroute -n 10.10.30.100

serverr2 and serverr3
traceroute -n 10.10.30.100
traceroute -n 10.10.20.100

Traceroute expectations

ClientVM → serverr2 should show R1 (192.168.57.254) then R2 (10.10.12.2) then destination.

ClientVM → serverr3 should show R1 (192.168.57.254) then R2 (10.10.12.2) then R3 (10.10.23.2) then destination.

## 9) Appendix A: Netplan YAML Files (Verbatim)
### 1) client.yaml
```.yaml
network:
  version: 2
  renderer: networkd
  ethernets:
    enp0s3:
      dhcp4: false
      addresses:
        - 192.168.57.100/24
      routes:
        - to: default
          via: 192.168.57.254
```

### 2) r1.yaml
```.yaml
network:
  version: 2
  renderer: networkd
  ethernets:
    enp0s3:
      dhcp4: false
      addresses:
        - 192.168.57.254/24
    enp0s8:
      dhcp4: false
      addresses:
        - 10.10.12.1/30
      routes:
        - to: 10.10.20.0/24
          via: 10.10.12.2
        - to: 10.10.30.0/24
          via: 10.10.12.2
        - to: 10.10.23.0/30
          via: 10.10.12.2
```
### 3) r2.yaml
```.yaml
network:
  version: 2
  renderer: networkd
  ethernets:
    enp0s3:
      dhcp4: false
      addresses:
        - 10.10.12.2/30
      routes:
        - to: 192.168.57.0/24
          via: 10.10.12.1
    enp0s8:
      dhcp4: false
      addresses:
        - 10.10.23.1/30
      routes:
        - to: 10.10.30.0/24
          via: 10.10.23.2
    enp0s9:
      dhcp4: false
      addresses:
        - 10.10.20.1/24
```
### 4) r3.yaml
```.yaml
network:
  version: 2
  renderer: networkd
  ethernets:
    enp0s3:
      dhcp4: false
      addresses:
        - 10.10.23.2/30
      routes:
        - to: 192.168.57.0/24
          via: 10.10.23.1
        - to: 10.10.20.0/24
          via: 10.10.23.1
    enp0s8:
      dhcp4: false
      addresses:
        - 10.10.30.1/24
```

### 5) serverr2.yaml
```.yaml
network:
  version: 2
  renderer: networkd
  ethernets:
    enp0s3:
      dhcp4: false
      addresses:
        - 10.10.20.100/24
      routes:
        - to: default
          via: 10.10.20.1
```

### 6) serverr3.yaml
```.yaml
network:
  version: 2
  renderer: networkd
  ethernets:
    enp0s3:
      dhcp4: false
      addresses:
        - 10.10.30.100/24
      routes:
        - to: default
          via: 10.10.30.1
```

## 10) Appendix B: Routing Persistence Script (Verbatim)
### 7) persistentRouting.sh
```bash
sudo tee /etc/sysctl.d/99-router.conf >/dev/null <<'EOF'
net.ipv4.ip_forward=1
EOF
sudo sysctl --system
sysctl net.ipv4.ip_forward

sudo tee -a /etc/sysctl.d/99-router.conf >/dev/null <<'EOF'
net.ipv4.conf.all.rp_filter=0
net.ipv4.conf.default.rp_filter=0
EOF
sudo sysctl --system
sysctl net.ipv4.conf.all.rp_filter
sysctl net.ipv4.conf.default.rp_filter

sudo netplan generate
sudo netplan apply
```

##11) Appendix C: Assumptions / Unknowns

This section is limited to items not explicitly stated in the provided inputs.

VirtualBox internal network names for the segments corresponding to:

10.10.12.0/30 (R1↔R2 transit)

10.10.23.0/30 (R2↔R3 transit)

10.10.20.0/24 (Server LAN S2)

10.10.30.0/24 (Server LAN S3)

The topology diagram uses descriptive labels (e.g., “net12”, “net23”, “S2”, “S3”), but the exact internal network identifiers as configured in VirtualBox are not included in the artifacts.

Distribution/OS version details (e.g., Ubuntu release) and any host OS routing specifics are not provided and are not assumed.
