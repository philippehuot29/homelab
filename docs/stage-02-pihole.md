# Stage 2 — OpenDNS & Ad Blocking (Pi-hole)

## Goal
Deploy Pi-hole in Docker as primary DNS resolver. Configure OpenDNS upstream. Network-wide ad blocking.

## Skills Developed
Docker volumes and port mapping, DNS resolution flow, recursive vs authoritative resolvers, container lifecycle management.

**Network+ relevance:** DNS resolution flow, recursive resolvers, network services
**Security+ relevance:** DNS filtering, threat mitigation, network hardening

---

## Architecture
```
Device → Router → Pi-hole (192.168.8.64:53) → OpenDNS (208.67.222.222) → Internet
```

Pi-hole runs in Docker using **host networking mode** — required because bridge networking causes port 53 conflicts with systemd-resolved and Docker's internal DNS.

---

## Pre-requisites

### Disable systemd-resolved
```bash
sudo systemctl stop systemd-resolved
sudo systemctl disable systemd-resolved
sudo rm /etc/resolv.conf
echo "nameserver 208.67.222.222" | sudo tee /etc/resolv.conf
sudo chattr +i /etc/resolv.conf  # make immutable
```

### Configure Docker daemon
```bash
# /etc/docker/daemon.json
{
  "iptables": false
}
```

---

## Deployment

**File:** `~/pihole/docker-compose.yml`
```yaml
services:
  pihole:
    container_name: pihole
    image: pihole/pihole:latest
    network_mode: host
    environment:
      TZ: 'Europe/Zagreb'
      WEBPASSWORD: '[redacted]'
      PIHOLE_DNS_1: '208.67.222.222'
      PIHOLE_DNS_2: '208.67.220.220'
    volumes:
      - '/mnt/storage/pihole/etc-pihole:/etc/pihole'
      - '/mnt/storage/pihole/etc-dnsmasq.d:/etc/dnsmasq.d'
    restart: unless-stopped
```
```bash
cd ~/pihole
docker compose up -d
```

---

## Configuration

### Upstream DNS
- Primary: `208.67.222.222` (OpenDNS)
- Secondary: `208.67.220.220` (OpenDNS)

### Blocklists
| List | Description |
|------|-------------|
| StevenBlack Unified | Consolidated hosts file — ads, malware, tracking |
| OISD Gold Standard | Balanced blocklist — low false positives, high coverage |

### Router DNS
Set router primary DNS to `192.168.8.64` so all network devices use Pi-hole automatically.

---

## Checklist
- [x] Disable systemd-resolved (port 53 conflict)
- [x] Make `/etc/resolv.conf` immutable
- [x] Configure `/etc/docker/daemon.json` (`iptables: false`)
- [x] Deploy Pi-hole via Docker Compose (host networking)
- [x] Set upstream DNS to OpenDNS
- [x] Configure router to use Pi-hole as primary DNS
- [x] Verify ad blocking on all devices
- [x] Configure custom blocklists (StevenBlack + OISD Gold)
- [x] Take Timeshift snapshot: Stage 2 complete

---

## Verification
```bash
# Check Pi-hole is listening on port 53
sudo ss -tlnp | grep 53

# Test DNS resolution through Pi-hole
dig google.com @192.168.8.64

# Check container health
docker ps | grep pihole
```

---

## Key Decisions
- **Host networking over bridge** — Pi-hole needs direct access to port 53; bridge mode causes conflicts with systemd-resolved and Docker DNS
- **OpenDNS upstream** — reliable, fast, with built-in malware/phishing protection layer
- **OISD Gold over Full** — OISD provides excellent coverage with significantly fewer false positives than the Full list

---

## Lessons Learned
- `chattr +i` on `/etc/resolv.conf` prevents Docker, systemd, and network managers from overwriting the DNS config on reboot
- Pi-hole dashboard accessible at `http://192.168.8.64/admin` — useful for monitoring query logs and identifying blocked domains
- libvirt's built-in dnsmasq conflicts with Pi-hole on port 53 — disable libvirt's default network before deploying Pi-hole (relevant for Stage 6)

---

*[← Stage 1](stage-01-linux.md) | [Back to README](../README.md) | [→ Stage 3](stage-03-wireguard.md)*
