# 🖥️ Philippe's Home Lab - Lenovo ThinkCentre M710q Tiny

> A hands-on network security home lab built on a Lenovo M710q Tiny, designed to bridge theoretical knowledge (CompTIA Network+, Security+) with real-world practical skills in Linux, networking, containerization, security, and automation.

---

## Hardware

| Component | Spec |
|-----------|------|
| **Machine** | Lenovo ThinkCentre M710q Tiny |
| **CPU** | Intel i5-6500T (4 cores, 2.5GHz, 35W TDP) |
| **RAM** | 16GB (2x8GB) Samsung/Hynix DDR4-2400 SO-DIMM CL17 |
| **Storage** | 250GB NVMe M.2 (Samsung 970 EVO Plus, OS) + 128GB SATA SSD (data/storage) |
| **Network** | 1x Intel I219-LM Gigabit LAN |
| **Expansion** | Lenovo Tiny optical bay chassis (adds 1x additional 2.5" SATA bay) |
| **Ports** | 6x USB 3.1, 1x COM DB-9, 2x DisplayPort, 1x LAN |
| **Power** | Original Lenovo 65W adapter |

### Maximum Specs (Hardware Ceiling)
- **RAM:** 32GB (2x 16GB DDR4 SO-DIMM) — DDR4-2400 or 3200MHz both compatible
- **CPU:** i5-6500T — **cannot be upgraded** (soldered BGA)
- **Storage:** M.2 NVMe (up to 2TB) + 2.5" SATA SSD + 2.5" HDD via expansion chassis simultaneously

### Planned Hardware Upgrades
- [x] RAM: Add 1x 8GB DDR4 SO-DIMM (→ 16GB dual-channel)
- [x] Storage: Add 256GB M.2 NVMe SSD for OS, repurpose SATA SSD for VMs
- [ ] RAM: Upgrade to 2x 16GB (→ 32GB) when VM workloads demand it

---

## Operating System

**Ubuntu Server 24.04 LTS** — installed headless via autoinstall (cloud-init)

Initial setup used Ubuntu Desktop for learning comfort, migrated to Server once CLI proficiency was established.

---

## Roadmap & Lab Stages

### ✅ Stage 0 — Hardware Acquisition & Assessment
- [x] Sourced refurbished M710q Tiny
- [x] Verified internals: RAM rank (1Rx8), M.2 slot availability, expansion chassis
- [x] Documented maximum upgrade path
- [x] Upgrade RAM to 16GB (matched Hynix 1Rx8 DDR4-2400)
- [x] Install 250GB NVMe M.2 SSD (Samsung 970 EVO Plus)

---

### ✅ Stage 1 — Linux Foundation
**Goal:** Install Ubuntu Server 24.04 LTS, harden SSH, configure firewall, install Docker.

- [x] Install Ubuntu Server 24.04 LTS on NVMe
- [x] Configure static IP address
- [x] Enable and harden SSH (key-based auth, disable root login, MaxAuthTries 3)
- [x] Configure Uncomplicated Firewall (UFW)(ports 22, 53, 80, 443, 51820)
- [x] Install Docker + Docker Compose
- [x] Install fail2ban (3-attempt ban)
- [x] Create homelab directory structure ~/homelab/{docker,scripts,configs,backups,docs}
- [x] Take Timeshift snapshot: Stage 0 baseline

**Skills developed:** Linux CLI fundamentals, SSH hardening, UFW firewall, static IP configuration, Docker engine

**Network+ relevance:** host configuration, basic security

**Security+ relevance:** hardening, least privilege

---

### ✅ Stage 2 — OpenDNS & Ad Blocking (Pi-hole)
**Goal:** First live network service. Deploy Pi-hole in Docker as primary DNS resolver. Configure OpenDNS upstream. Network-wide ad blocking.

- [x] Disable systemd-resolved (port 53 conflict)
- [x] Make /etc/resolv.conf immutable
- [x] Configure /etc/docker/daemon.json (iptables: false)
- [x] Deploy Pi-hole via Docker Compose
- [x] Set upstream DNS to OpenDNS
- [x] Configure as primary DNS resolver for home network
- [x] Explore Pi-hole query logs and statistics dashboard
- [x] Configure custom blocklists (OISD Gold Standard List)
- [x] Verify ad blocking on all devices
- [x] Take Timeshift snapshot: Stage 2 complete


**Skills developed:** Docker basics (volumes, port mapping, networking), DNS resolution flow, recursive vs authoritative resolvers, container lifecycle management

**Network+ relevance:** DNS resolution flow, recursive resolvers

**Security+ relevance:** DNS filtering, threat mitigation

---

### ✅ Stage 3 — VPN Server (WireGuard)
**Goal:** Self-hosted VPN accessible from anywhere. Eliminate reliance on commercial VPN providers.

- [x] Install WireGuard (kernel module — no Docker needed)
- [x] Generate server and client key pairs
- [x] Configure peer tunnels for remote devices
- [x] Configure DuckDNS for dynamic IP tracking
- [x] Test connectivity from mobile and laptop externally
- [x] Take Timeshift snapshot: Stage 3 complete


**Skills developed:** VPN fundamentals, asymmetric key cryptography, tunnel configuration, firewall rules, NAT traversal

**Security+ relevance:** Tunneling protocols, IPSec vs. WireGuard vs. OpenVPN comparison, encryption key management

---

### 🔄 Stage 4 — Firewall Lab (pfSense/OPNsense — Learning Mode)
**Goal:** Learn enterprise firewall concepts safely without touching live network traffic.

> **Architecture note:** Running as a VM in isolated learning mode — not acting as network gateway. Single NIC machine cannot function as a proper router without a USB NIC addition. This decision is intentional and can be revisited.

- [ ] Install pfSense or OPNsense in a KVM/QEMU VM
- [ ] Build firewall rule sets (allow/deny by port, protocol, IP range)
- [ ] Configure NAT rules
- [ ] Explore VLAN concepts and inter-VLAN routing logic
- [ ] Study IDS/IPS integration options

**Skills developed:** VM management, firewall rule logic, NAT, VLAN theory

**Security+ relevance:** Network security controls, stateful vs. stateless firewalls, DMZ architecture

**Future path:** Add USB NIC → promote pfSense to actual network gateway

---

### 🔄 Stage 5 — Personal Cloud (Nextcloud)
**Goal:** Self-hosted cloud storage using 2TB USB HDD as backend.

- [ ] Deploy Nextcloud in Docker
- [ ] Mount 2TB USB HDD as persistent storage volume
- [ ] Configure Nginx reverse proxy
- [ ] Obtain HTTPS certificate via Let's Encrypt (Certbot or Nginx Proxy Manager)
- [ ] Set up automated backup script (Python/bash) to secondary location

**Skills developed:** Reverse proxying, SSL/TLS certificate management, Docker volumes, storage management

---

### 🔄 Stage 6 — Web Hosting & Portfolio Site
**Goal:** Host a personal site or project documentation publicly. Reinforce professional presence.

- [ ] Configure Nginx to serve static site
- [ ] Point a domain (or DuckDNS subdomain) at home IP
- [ ] Set up dynamic DNS updater if ISP provides dynamic IP
- [ ] Implement HTTPS with Let's Encrypt
- [ ] Explore hosting a portfolio site or network-security-portfolio documentation site

**Skills developed:** DNS management, web server configuration, SSL/TLS, dynamic DNS

---

### 🔄 Stage 7 — Monitoring & Observability
**Goal:** Make the homelab feel like a real NOC environment.

- [ ] Deploy Grafana + Prometheus for system and container metrics
- [ ] Add Uptime Kuma for service availability monitoring
- [ ] Configure alerting (email or Telegram notifications when services go down)
- [ ] Build network traffic dashboard (Ntopng or Grafana + InfluxDB)

**Skills developed:** Metrics collection, dashboard design, alerting pipelines, time-series data

**Telecoms relevance:** Directly mirrors NOC monitoring workflows

---

### 🔄 Stage 8 — Intrusion Detection (Suricata)
**Goal:** Network-based IDS inspecting live traffic. Security+ hands-on complement.

- [ ] Install Suricata on host (not Docker — needs raw interface access)
- [ ] Configure rules and threat signatures
- [ ] Pipe alerts into a log aggregator or Grafana
- [ ] Tune rules to reduce false positives

**Skills developed:** IDS/IPS configuration, signature-based detection, network traffic analysis

**Security+ relevance:** IDS vs. IPS, signature vs. anomaly detection, SIEM concepts

---

### 🔄 Stage 9 — Vulnerability Lab (Ethical Hacking Practice)
**Goal:** Legal, isolated environment to practice offensive security concepts from the defense side.

- [ ] Deploy DVWA (Damn Vulnerable Web Application) in isolated Docker network
- [ ] Deploy Metasploitable VM in isolated network segment
- [ ] Practice common attack vectors: SQL injection, XSS, privilege escalation
- [ ] Document findings and remediations

> ⚠️ All practice is conducted in isolated, self-owned lab environments. No external targets.

**Skills developed:** Penetration testing methodology, OWASP Top 10, vulnerability assessment

**Security+ relevance:** Attack types, vulnerability scanning, ethical hacking concepts

---

### 🔄 Stage 10 — Identity & Authentication (Authentik)
**Goal:** Self-hosted SSO and identity provider. Enterprise-grade auth concepts in the lab.

- [ ] Deploy Authentik in Docker
- [ ] Configure OAuth2 / OpenID Connect for lab services
- [ ] Integrate with Nextcloud and Grafana for single sign-on
- [ ] Explore LDAP and SAML integration options

**Skills developed:** IAM concepts, OAuth2/OIDC flows, SSO architecture

**Security+ relevance:** Authentication protocols, identity federation, MFA

---

### 🔄 Stage 11 — Git Server & CI Automation (Gitea)
**Goal:** Self-hosted Git with webhook-driven automation.

- [ ] Deploy Gitea in Docker
- [ ] Mirror network-security-portfolio repository locally
- [ ] Configure webhooks for automated actions
- [ ] Write Python automation scripts triggered by commits

**Skills developed:** Git internals, webhook pipelines, SSH key management, Python automation

---

### 🔄 Stage 12 — Home Automation (Home Assistant)
**Goal:** IoT protocol exposure and API-driven automation.

- [ ] Deploy Home Assistant in Docker
- [ ] Integrate available smart devices
- [ ] Explore MQTT protocol
- [ ] Build automations using the HA scripting engine

**Skills developed:** IoT protocols (MQTT, Zigbee), API integrations, event-driven automation

---

## Python & Automation Projects

Organic automation tasks generated by the lab itself — more motivating than tutorials because they're real infrastructure:

| Script | Purpose |
|--------|---------|
| `container_health_check.py` | Check all Docker containers are running, send Telegram alert if not |
| `pihole_weekly_report.py` | Parse Pi-hole logs, generate blocked domain summary |
| `backup_nextcloud.sh` | Automated Nextcloud data backup to USB HDD on schedule |
| `update_containers.py` | Pull latest images and recreate all containers with one command |
| `ddns_updater.py` | Check public IP and update DuckDNS if changed |

---

## RAM Planning Reference

Estimated idle RAM footprint for full stack:

| Service | Idle RAM |
|---------|----------|
| Ubuntu Server base | ~400MB |
| Pi-hole (Docker) | ~75MB |
| WireGuard | ~0MB (kernel) |
| Nextcloud stack | ~700MB |
| Nginx | ~75MB |
| Grafana + Prometheus | ~500MB |
| Suricata | ~400MB |
| Authentik | ~750MB |
| Gitea | ~200MB |
| Uptime Kuma | ~100MB |
| pfSense VM | ~512MB |
| **Total (conservative)** | **~3.7GB** |
| **With headroom & spikes** | **~6-8GB** |

> **Conclusion:** 16GB handles the full stack comfortably. 32GB becomes relevant when adding multiple full VMs simultaneously.

---

## Upgrade Path

```
Previously:  8GB RAM  |  128GB SATA SSD  |  No M.2    
Step 1:  16GB RAM  |  128GB SATA SSD  |  No M.2        
Step 2:  16GB RAM  |  128GB SATA SSD  |  256GB NVMe  
Step 3:  32GB RAM  |  128GB SATA SSD  |  256GB NVMe     
```

---

## Learning Goals

- **Linux:** Ubuntu Server proficiency, CLI fluency, scripting
- **Networking:** Practical application of CompTIA Network+ concepts
- **Security:** CompTIA Security+ hands-on complement (target: April 2026)
- **Containers:** Docker, Docker Compose, container networking
- **Automation:** Python scripting, bash, cron, webhooks
- **Cloud:** Bridge to AWS Cloud Practitioner knowledge via self-hosted equivalents

---

## Repository Structure (Planned)

```
homelab/
├── README.md                  # This file
├── docker/
│   ├── pihole/
│   ├── nextcloud/
│   ├── grafana/
│   ├── wireguard/
│   └── authentik/
├── scripts/
│   ├── backup/
│   ├── monitoring/
│   └── automation/
├── configs/
│   ├── nginx/
│   ├── ufw/
│   └── wireguard/
└── docs/
    ├── stage-1-setup.md
    ├── stage-2-pihole.md
    └── ...
```

---

*Built and maintained by Philippe | Network & Security Professional | CompTIA Network+ | AWS Cloud Practitioner | Security+ (target April 2026)*
