# Stage 1 — Linux Foundation

## Goal
Install Ubuntu Server 24.04 LTS, harden SSH, configure firewall, install Docker.

## Skills Developed
Linux CLI fundamentals, SSH hardening, UFW firewall, static IP configuration, Docker engine.

**Network+ relevance:** Host configuration, basic network security
**Security+ relevance:** System hardening, least privilege, access control

---

## Installation

- **OS:** Ubuntu Server 24.04 LTS (headless, no GUI)
- **Install method:** USB bootable via Rufus
- **Hostname:** `homelab`
- **User:** `cyberphil`
- **IP:** `192.168.8.64` (reserved on router)
- **SSH:** Enabled during install

---

## Configuration Steps

### Static IP
Reserved via router DHCP reservation (MAC: `6c:4b:90:5e:aa:34`) rather than static netplan config — allows DHCP flexibility while maintaining predictable address.

### SSH Hardening
```bash
# /etc/ssh/sshd_config changes
PermitRootLogin no
PasswordAuthentication yes  # key-based auth planned
MaxAuthTries 3
```

### UFW Firewall
```bash
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow 22/tcp      # SSH
sudo ufw allow 53/tcp      # Pi-hole DNS
sudo ufw allow 53/udp      # Pi-hole DNS
sudo ufw allow 80/tcp      # Pi-hole admin
sudo ufw allow 443/tcp     # HTTPS (future)
sudo ufw allow 51820/udp   # WireGuard
sudo ufw enable
```

### fail2ban
```bash
# 3-attempt ban, default jail on SSH
sudo apt install fail2ban
```

### Docker
```bash
sudo apt install docker.io docker-compose
sudo usermod -aG docker cyberphil
```

### Directory Structure
```
~/homelab/
├── docker/       # Docker Compose files per service
├── scripts/      # Automation scripts
├── configs/      # Service configuration files
├── backups/      # Backup outputs
└── docs/         # Documentation
```

---

## Checklist
- [x] Install Ubuntu Server 24.04 LTS on NVMe
- [x] Configure static IP (192.168.178.64 via DHCP reservation)
- [x] Enable and harden SSH (disable root login, MaxAuthTries 3)
- [x] Configure UFW (ports 22, 53, 80, 443, 51820)
- [x] Install Docker + Docker Compose
- [x] Install fail2ban (3-attempt ban)
- [x] Create homelab directory structure
- [x] Take Timeshift snapshot: Stage 1 baseline

---

## Key Decisions
- Chose headless Ubuntu Server over Desktop for lower RAM footprint and production-like environment
- Used DHCP reservation over static netplan for flexibility — router controls IP assignment
- Installed fail2ban immediately after SSH — brute force protection before any services exposed
- Set `DEFAULT_FORWARD_POLICY=ACCEPT` in UFW for WireGuard NAT forwarding (Stage 3)

---

## Lessons Learned
- `systemd-resolved` conflicts with Pi-hole on port 53 — must be disabled before Stage 2
- Docker's default iptables management conflicts with UFW — configure `/etc/docker/daemon.json` with `"iptables": false` before deploying containers

---

*[← Back to README](../README.md) | [→ Stage 2](stage-02-pihole.md)*
