# 🖥️ Philippe's Home Lab - Lenovo ThinkCentre M710q Tiny

> A hands-on network security home lab built on a Lenovo M710q Tiny, designed to bridge theoretical knowledge (CompTIA Network+, Security+) with real-world practical skills in Linux, networking, containerization, security, and automation.

---

## Hardware

| Component | Spec |
|-----------|------|
| **Machine** | Lenovo ThinkCentre M710q Tiny |
| **CPU** | Intel i5-6500T — 4 cores/4 threads, 2.5GHz/3.1GHz (Based/Max Freq) , 6 MB cache, HD 530 Integrated Graphics |
| **RAM** | 16GB (2x8GB) Samsung/Hynix DDR4-2400 SO-DIMM CL17 |
| **Storage** | 250GB NVMe M.2 (Samsung 970 EVO Plus, OS) + 128GB SATA SSD (data/storage) |
| **Network** | 1x Intel I219-LM Gigabit LAN |
| **Expansion** | Lenovo Tiny optical bay chassis (adds 1x additional 2.5" SATA bay) |
| **Ports** | 6x USB 3.1, 1x COM DB-9, 2x DisplayPort, 1x LAN |
| **Power** | Original Lenovo 65W adapter |

### Maximum Specs (Hardware Ceiling)
- **RAM:** 32GB (2x 16GB DDR4 SO-DIMM) — DDR4-2400Mhz
- **CPU:** i5-6500T — upgradeable to Core i7-7700T — 4 cores/8 threads, 2.9GHz/3.8GHz (Based/Max Freq) , 8 MB cache, HD 630 Integrated Graphics
- **Storage:**
    - M.2 NVMe Solid State Drive (SSD) / PCIe NVMe, PCIe 3.0 x 4, 32Gb/s
    - 2.5" Solid State Drive (SSD) / SATA 6.0Gb/s, 2.5"
    - 2.5" HDD via expansion chassis simultaneously

### Planned Hardware Upgrades
- [x] RAM: Add 1x 8GB DDR4 SO-DIMM (→ 16GB dual-channel)
- [x] Storage: Add 256GB M.2 NVMe SSD for OS, repurpose SATA SSD for VMs
- [x] GL.iNet Beryl 7 Router
- [ ] Managed switch Tp-Link TL-SG608E 8-Port Gigabit 
- [ ] CPU: Upgrade to Intel i7-7700T
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

**Skills developed:** Linux CLI fundamentals, SSH hardening, UFW firewall, static IP configuration, Docker engine

**Network+ relevance:** host configuration, basic security

**Security+ relevance:** hardening, least privilege

- [x] Install Ubuntu Server 24.04 LTS on NVMe
- [x] Configure static IP address
- [x] Enable and harden SSH (key-based auth, disable root login, MaxAuthTries 3)
- [x] Configure Uncomplicated Firewall (UFW)(ports 22, 53, 80, 443, 51820)
- [x] Install Docker + Docker Compose
- [x] Install fail2ban (3-attempt ban)
- [x] Create homelab directory structure ~/homelab/{docker,scripts,configs,backups,docs}
- [x] Take Timeshift snapshot: Stage 0 baseline

---

### ✅ Stage 2 — OpenDNS & Ad Blocking (Pi-hole)
**Goal:** First live network service. Deploy Pi-hole in Docker as primary DNS resolver. Configure OpenDNS upstream. Network-wide ad blocking.

**Skills developed:** Docker basics (volumes, port mapping, networking), DNS resolution flow, recursive vs authoritative resolvers, container lifecycle management

**Network+ relevance:** DNS resolution flow, recursive resolvers

**Security+ relevance:** DNS filtering, threat mitigation

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

---

### ✅ Stage 3 — VPN Server (WireGuard)
**Goal:** Self-hosted VPN accessible from anywhere. Eliminate reliance on commercial VPN providers.

**Skills developed:** VPN fundamentals, asymmetric key cryptography, tunnel configuration, firewall rules, NAT traversal

**Security+ relevance:** Tunneling protocols, IPSec vs. WireGuard vs. OpenVPN comparison, encryption key management

- [x] Install WireGuard (kernel module — no Docker needed)
- [x] Generate server and client key pairs
- [x] Configure peer tunnels for remote devices
- [x] Configure DuckDNS for dynamic IP tracking
- [x] Test connectivity from mobile and laptop externally
- [x] Take Timeshift snapshot: Stage 3 complete

---

### ✅ Stage 4 — GL-inet Beryl 7 Integration
**Goal:** GL-inet Beryl 7 becomes the network layer between devices and ISP Router. DNS pointed to M710q Pi-hole.

**Skills developed:** Router gateway architecture, DNS forwarding, double NAT, VPN kill switch, repeater mode for mobile use

**Network+ relevance:** Gateway configuration, NAT, DNS forwarding

- [x] Connect Beryl 7 WAN port to ISP Router LAN port
- [x] Set Beryl 7 DNS to M710q IP (192.168.178.64)
- [x] Verify all devices behind Beryl 7 use Pi-hole
- [x] Configure GL-inet SSID to generic name
- [x] Enable VPN kill switch in GL-inet admin
- [x] Test repeater mode (WiFi-as-WAN) at a café

---

### ✅ Stage 5 — Exit Node (GL-inet Brume 3)
**Goal:** Brume 3 at residential address running WireGuard server. GL-inet Beryl 7 tunnels through it. Residential IP when traveling.

**Skills developed:** WireGuard server config, DuckDNS dynamic DNS, port forwarding, GL-inet GoodCloud monitoring, VPN kill switch

**Security+ relevance:** VPN architecture, remote access security, network privacy

- [x] Configure WireGuard server on Brume 3
- [x] Configure DuckDNS dynamic DNS on Brume 3
- [x] Set port forwarding on ISP router (UDP 51820 → Brume 3)
- [x] Configure Beryl 7 WireGuard client → Brume 3 tunnel
- [x] Enable kill switch on Beryl 7
- [x] Verify residential IP when traveling
- [x] Add both routers to GoodCloud for remote monitoring

---

### 🔄 Stage 6 — Firewall Lab (OPNsense VM)
**Goal:** OPNsense 25.1 in KVM/QEMU VM. Build firewall rule sets, NAT, VLANs. Promote to full network gateway with USB NIC and managed switch.

**Skills developed:** VM management (KVM/QEMU/libvirt), Linux bridge networking, firewall rule logic, NAT, VLAN theory, DMZ architecture

**Security+ relevance:** Stateful vs stateless firewalls, DMZ, network segmentation, IDS/IPS integration

> **Architecture note:** OPNsense running as a KVM/QEMU VM, accessible at 192.168.178.72 via Linux bridge (br0). USB NIC and managed switch pending arrival to enable proper WAN/LAN separation and promote OPNsense to full network gateway.

- [x] Install KVM/QEMU/libvirt on Ubuntu Server
- [x] Configure Linux bridge (br0) replacing macvtap
- [x] Deploy OPNsense 25.1 VM (4GB RAM, 16GB disk, SATA/q35)
- [x] Update WireGuard PostUp/PostDown rules for br0
- [x] OPNsense accessible at 192.168.178.72 via WireGuard tunnel
- [ ] Install USB NIC and managed switch (TL-SG608E)
- [ ] Build allow/deny firewall rule sets (port, protocol, IP range)
- [ ] Configure NAT rules
- [ ] Explore VLAN concepts and inter-VLAN routing
- [ ] Document IDS/IPS integration options

---

### 🔜 Stage 7 — Telecom & AI Lab (FreeSWITCH + SWAIG)
**Goal:** FreeSWITCH PBX with SIP client. FastAPI + PostgreSQL SWAIG function lab. AI-driven call flows combining telecoms background with modern AI.

**Skills developed:** SIP protocol, VoIP architecture, FastAPI, PostgreSQL, AI function calling, SignalWire SDK

> Requires 16GB RAM (confirmed). Deploy after RAM stability confirmed under full load.

- [ ] Deploy FreeSWITCH in Docker
- [ ] Configure Zoiper SIP client on laptop for test calls
- [ ] Build FastAPI SWAIG function endpoint
- [ ] Connect PostgreSQL for call data persistence
- [ ] Build AI-driven IVR demo using SignalWire AI Agent SDK
- [ ] Document on GitHub with architecture diagram

---

### 🔜 Stage 8 — Personal Cloud (Nextcloud)
**Goal:** Self-hosted cloud storage using 2TB USB HDD as backend.

- [ ] Deploy Nextcloud in Docker
- [ ] Mount 2TB USB HDD as persistent storage volume
- [ ] Configure Nginx reverse proxy
- [ ] Obtain HTTPS certificate via Let's Encrypt (Certbot or Nginx Proxy Manager)
- [ ] Set up automated backup script (Python/bash) to secondary location

**Skills developed:** Reverse proxying, SSL/TLS certificate management, Docker volumes, storage management

---

### 🔜 Stage 9 — Web Hosting & Portfolio Site
**Goal:** Host a personal site or project documentation publicly. Reinforce professional presence.

- [ ] Configure Nginx to serve static site
- [ ] Point a domain (or DuckDNS subdomain) at home IP
- [ ] Set up dynamic DNS updater if ISP provides dynamic IP
- [ ] Implement HTTPS with Let's Encrypt
- [ ] Explore hosting a portfolio site or network-security-portfolio documentation site

**Skills developed:** DNS management, web server configuration, SSL/TLS, dynamic DNS

---

### 🔜 Stage 10 — Infrastructure as Code (Terraform + Ansible)
**Goal:** Terraform for infrastructure provisioning. Ansible for configuration management. All configs version-controlled in Git.

**Skills developed:** IaC principles, Terraform HCL, Ansible playbooks, idempotent configuration, version-controlled infrastructure

**Career relevance:** Cloud Network Engineer, SRE, Platform Engineer

- [ ] Create GitHub repo for homelab IaC
- [ ] Write Terraform configs for all existing Docker services
- [ ] Write Ansible playbook for M710q base configuration
- [ ] Automate Timeshift snapshots via Ansible
- [ ] Document IaC architecture in README

---

### 🔜 Stage 11 — CI/CD Pipeline (GitHub Actions)
**Goal:** GitHub Actions pipeline for homelab service deployment. Automated testing of infrastructure changes.

**Skills developed:** CI/CD concepts, YAML pipeline definition, automated testing, webhook triggers, deployment automation

**Career relevance:** Directly differentiates from NetAdmin roles. Every DevOps/SRE role uses CI/CD.

- [ ] Set up GitHub Actions workflow for Docker Compose deployment
- [ ] Add linting/validation step for Terraform configs
- [ ] Configure self-hosted GitHub Actions runner on M710q
- [ ] Automate portfolio site deployment on git push
- [ ] Add Telegram notification on pipeline success/failure

---

### 🔜 Stage 12 — Monitoring & Observability (Grafana Stack)
**Goal:** Grafana + Prometheus for metrics. Uptime Kuma for availability. Loki for log aggregation. Telegram alerts on service failures.

**Skills developed:** Metrics collection, dashboard design, alerting pipelines, time-series data, PromQL basics, log aggregation

**Network+ relevance:** Network monitoring, SNMP

**Telecoms relevance:** Directly mirrors NOC monitoring workflows

- [ ] Deploy Grafana + Prometheus in Docker
- [ ] Add Node Exporter for system metrics (CPU, RAM, disk)
- [ ] Add cAdvisor for Docker container metrics
- [ ] Deploy Uptime Kuma for service availability monitoring
- [ ] Configure Telegram alerting (service down, high CPU)
- [ ] Build network traffic dashboard (Ntopng or InfluxDB)
- [ ] Add Loki for log aggregation (integrates with Grafana)

---

### 🔜 Stage 13 — OpenClaw AI Agent Gateway
**Goal:** OpenClaw in Docker, accessible via Telegram. Six-agent squad for job search automation and homelab monitoring.

**Skills developed:** Node.js service management, AI agent architecture, API integration, Docker isolation, agentic workflows

**Cost:** ~$2–4 USD/month via Claude API

| Agent | Role |
|-------|------|
| Scout | Job board intel & daily digest |
| Tailor | Resume & cover letter generation |
| Tracker | Application CRM + Gmail monitoring |
| Coach | Interview prep & mock sessions |
| Publisher | LinkedIn content scheduling |
| Sentinel | Homelab & tunnel monitoring |

- [ ] Deploy OpenClaw in isolated Docker container
- [ ] Obtain Claude API key (console.anthropic.com)
- [ ] Run OpenClaw onboard wizard — configure Telegram gateway
- [ ] Deploy Sentinel agent (homelab + tunnel monitoring)
- [ ] Deploy Scout agent (daily job board digest)
- [ ] Deploy Tracker agent (application CRM + Gmail monitoring)
- [ ] Deploy Tailor agent (resume + cover letter generation)
- [ ] Deploy Coach agent (interview prep + mock sessions)
- [ ] Deploy Publisher agent (LinkedIn content scheduling)

---

### 🔜 Stage 14 — Intrusion Detection (Suricata IDS)
**Goal:** Suricata on host (not Docker — needs raw interface access). Rules tuned, alerts piped to Grafana.

**Skills developed:** IDS/IPS configuration, signature-based detection, network traffic analysis, rule tuning, false positive reduction

**Security+ relevance:** IDS vs IPS, signature vs anomaly detection, SIEM concepts

- [ ] Install Suricata on host (apt install suricata)
- [ ] Configure interface for live traffic inspection
- [ ] Enable and update Emerging Threats rule set
- [ ] Pipe Suricata alerts to Grafana via log aggregator
- [ ] Build Grafana dashboard for IDS alerts
- [ ] Tune rules to reduce false positives
- [ ] Test detection with simulated attack from Kali VM

---

### 🔜 Stage 15 — SOC Capabilities (Wazuh + ELK Stack)
**Goal:** Wazuh SIEM + Elastic Stack for log aggregation. TheHive for incident response. MISP for threat intelligence.

**Skills developed:** SIEM architecture, log correlation, threat hunting, incident response workflow, IOC management

**Security+ relevance:** SIEM, threat intelligence, incident response. Strong signal for SOC Analyst roles.

> RAM-intensive — deploy after confirming 16GB is sufficient under load. Consider 32GB upgrade if needed.

- [ ] Deploy Wazuh manager + agent in Docker
- [ ] Deploy Elasticsearch + Kibana (Elastic Stack)
- [ ] Configure log ingestion from all homelab services
- [ ] Deploy TheHive for incident response tracking
- [ ] Deploy MISP for threat intelligence feeds
- [ ] Build correlation rules: Pi-hole DNS + Suricata + Wazuh
- [ ] Run a simulated incident and document response workflow
---

### 🔜 Stage 16 — Vulnerability Lab (DVWA + Metasploitable)
**Goal:** DVWA and Metasploitable in isolated Docker networks. Practice attack vectors, document remediations in portfolio format.

**Skills developed:** Penetration testing methodology, OWASP Top 10, SQL injection, XSS, privilege escalation, vulnerability assessment

**Security+ relevance:** Attack types, vulnerability scanning, ethical hacking concepts

> ⚠️ All practice conducted in isolated, self-owned lab environments. Never test external targets.

- [ ] Deploy DVWA in isolated Docker network (no internet access)
- [ ] Deploy Metasploitable VM in isolated network segment
- [ ] Install OWASP ZAP and run against DVWA
- [ ] Practice OWASP Top 10 attack categories
- [ ] Run Nessus or OpenVAS scan against lab targets
- [ ] Document each finding: attack vector, impact, remediation
- [ ] Write lab report in portfolio format
- [ ] Apply STRIDE threat modeling to one homelab service

---

### 🔜 Stage 17 — Cloud Security Integration (AWS)
**Goal:** AWS integration with homelab. CloudTrail, GuardDuty, Security Hub. Terraform to provision cloud resources.

**Skills developed:** AWS security services, hybrid cloud architecture, cloud monitoring, IAM, Terraform cloud provisioning

**Cert link:** AWS Cloud Practitioner (held). Bridges to AWS Solutions Architect and Security Specialty.

- [ ] Provision AWS resources via Terraform (VPC, EC2, S3)
- [ ] Configure CloudTrail for audit logging
- [ ] Enable GuardDuty for threat detection
- [ ] Set up Security Hub for centralized findings
- [ ] Build CloudWatch → Grafana metrics pipeline
- [ ] Document hybrid homelab ↔ AWS architecture

---

### 🔜 Stage 18 — Identity & Authentication (Authentik)
**Goal:** Self-hosted SSO and identity provider. Enterprise-grade auth concepts in the lab.

- [ ] Deploy Authentik in Docker
- [ ] Configure OAuth2 / OpenID Connect for lab services
- [ ] Integrate with Nextcloud and Grafana for single sign-on
- [ ] Explore LDAP and SAML integration options

**Skills developed:** IAM concepts, OAuth2/OIDC flows, SSO architecture

**Security+ relevance:** Authentication protocols, identity federation, MFA

---

### 🔜 Stage 19 — Container Orchestration (K3s + Helm)
**Goal:** K3s lightweight Kubernetes on M710q. Helm charts for service deployment. ArgoCD for GitOps.

**Skills developed:** Kubernetes architecture, pod/service/deployment concepts, Helm charts, GitOps with ArgoCD, K8s security

**Career relevance:** Single most valuable DevOps/cloud skill. Opens Cloud Engineer, SRE, and Platform Engineer roles.

- [ ] Install K3s on M710q
- [ ] Deploy Pi-hole as a Kubernetes service (first migration)
- [ ] Write Helm charts for core homelab services
- [ ] Deploy ArgoCD for GitOps — Git push triggers K8s deployment
- [ ] Configure Kubernetes RBAC and network policies
- [ ] Deploy Falco for runtime security monitoring
---

### 🔜 Stage 20 — Git Server & CI Automation (Gitea)
**Goal:** Self-hosted Git with webhook-driven automation.

- [ ] Deploy Gitea in Docker
- [ ] Mirror network-security-portfolio repository locally
- [ ] Configure webhooks for automated actions
- [ ] Write Python automation scripts triggered by commits

**Skills developed:** Git internals, webhook pipelines, SSH key management, Python automation

---

### 🔜 Stage 21 — Home Automation (Home Assistant)
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
| `opnsense_backup.py` | Export OPNsense config via API and store versioned backup |
| `wireguard_peer_monitor.py` | Check WireGuard peer last handshake, alert if tunnel drops |
| `suricata_alert_parser.py` | Parse Suricata EVE JSON logs, push critical alerts to Telegram |

---

## RAM Planning Reference

Estimated idle RAM footprint for full stack:

| Service | Idle RAM |
|---------|----------|
| Ubuntu Server base | ~400MB |
| Pi-hole (Docker) | ~75MB |
| WireGuard | ~0MB (kernel) |
| OPNsense VM | ~1024MB (reduced from 4GB post-install) |
| Nextcloud stack | ~700MB |
| Nginx | ~75MB |
| Grafana + Prometheus + Loki | ~600MB |
| Uptime Kuma | ~100MB |
| Suricata (host) | ~400MB |
| Wazuh + ELK Stack | ~2GB |
| Authentik | ~750MB |
| Gitea | ~200MB |
| FreeSWITCH + FastAPI | ~500MB |
| K3s (lightweight Kubernetes) | ~500MB |
| **Total (conservative)** | **~8GB** |
| **With headroom & spikes** | **~10-12GB** |

> **Conclusion:** 16GB handles the full stack comfortably. 32GB becomes relevant when running Wazuh + ELK + multiple VMs simultaneously.

---

## Learning Goals

- **Linux:** Ubuntu Server proficiency, CLI fluency, scripting
- **Networking:** Practical application of CompTIA Network+ concepts
- **Security:** CompTIA Security+ hands-on complement (target: April 2026)
- **Containers:** Docker, Docker Compose, container networking, Kubernetes (K3s)
- **Automation:** Python scripting, bash, cron, webhooks, GitHub Actions CI/CD
- **Infrastructure as Code:** Terraform, Ansible, version-controlled infrastructure
- **Cloud:** Hybrid homelab ↔ AWS architecture, CloudTrail, GuardDuty, Security Hub
- **Monitoring:** Grafana, Prometheus, Loki, Uptime Kuma, NOC-style dashboards
- **Security Operations:** Suricata IDS, Wazuh SIEM, TheHive, MISP threat intel

---

## Repository Structure (Planned)
```
homelab/
├── README.md                    # This file
├── docker/
│   ├── pihole/
│   ├── nextcloud/
│   ├── grafana/
│   ├── wireguard/
│   ├── authentik/
│   ├── gitea/
│   ├── wazuh/
│   └── freeswitch/
├── scripts/
│   ├── backup/
│   ├── monitoring/
│   └── automation/
├── configs/
│   ├── nginx/
│   ├── ufw/
│   ├── wireguard/
│   └── opnsense/
├── terraform/
│   ├── docker-services/
│   └── aws/
├── ansible/
│   ├── m710q-base.yml
│   └── services.yml
└── docs/
    ├── stage-00-hardware.md
    ├── stage-01-linux.md
    ├── stage-02-pihole.md
    └── ...
```

---

*Built and maintained by Philippe | Network & Security Professional | CompTIA Network+ ✅ | AWS Cloud Practitioner ✅ | Security+ (target April 2026) 🔄*
