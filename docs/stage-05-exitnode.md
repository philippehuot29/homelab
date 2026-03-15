# Stage 5 — Exit Node (GL-inet Brume 3)

## Goal
GL-inet Brume 3 deployed at a residential location running WireGuard server. GL-inet Beryl 7 tunnels through it when a residential IP is needed. Failover via DigitalOcean VPS.

## Skills Developed
WireGuard server configuration, DuckDNS dynamic DNS, port forwarding, GL-inet GoodCloud monitoring, VPN kill switch, residential IP routing.

**Security+ relevance:** VPN architecture, remote access security, network privacy, tunneling protocols

---

## Architecture
```
Internet
    ↓
Residential ISP 
    ↓
ISP Router (port forwarding UDP 51820 → Brume 3)
    ↓
GL-inet Brume 3 — WireGuard SERVER (residential IP exit point)
    ↑
WireGuard tunnel
    ↑
GL-inet Beryl 7 — WireGuard CLIENT (remote location)
    ↑
Laptop / devices
```

When the Beryl 7 connects to the Brume 3, all outbound traffic exits through the residential ISP connection — appearing as a local residential IP to external services.

---

## Why GL-inet Brume 3

| Feature | Value |
|---------|-------|
| **Compact form factor** | Deck-of-cards size — unobtrusive at host location |
| **OpenWrt based** | Full Linux router, SSH accessible |
| **Built-in WireGuard server** | No additional software needed |
| **Low power** | ~3-5W idle — negligible electricity cost |
| **GoodCloud** | Remote monitoring without exposing SSH |
| **DuckDNS support** | Built-in dynamic DNS client |

---

## Configuration Steps

### 1. Physical Setup
```
Brume 3 WAN port → ISP router LAN port (ethernet)
Power adapter → outlet
```

### 2. DuckDNS Dynamic DNS
ISP residential connections use dynamic IPs — DuckDNS provides a stable hostname.

- Admin UI → More Settings → Dynamic DNS
- Provider: DuckDNS
- Domain: `[your-subdomain].duckdns.org`
- Token: `[redacted]`
- Update interval: 5 minutes

> **Security note:** Never commit DuckDNS tokens or subdomains to public repositories.

### 3. WireGuard Server on Brume 3
- Admin UI → VPN → WireGuard Server
- Enable WireGuard server
- Listen port: `51820`
- Server address: `10.1.0.1/24`
- Generate server keypair
- Add peer: Beryl 7 (import Beryl 7 public key)

### 4. Port Forwarding on ISP Router
Forward WireGuard traffic to Brume 3:
- Protocol: UDP
- External port: 51820
- Internal IP: Brume 3 LAN IP
- Internal port: 51820

> Some ISP routers lock down port forwarding. Verify this is available before deployment.

### 5. WireGuard Client on Beryl 7
- Admin UI → VPN → WireGuard Client
- Add new profile
- Endpoint: `[your-subdomain].duckdns.org:51820`
- Server public key: [Brume 3 public key]
- AllowedIPs: `0.0.0.0/0` (route all traffic through residential IP)

### 6. Enable Kill Switch on Beryl 7
- Admin UI → VPN → VPN Dashboard
- Enable kill switch for the Brume 3 tunnel
- All traffic blocked if tunnel drops

---

## Failover — DigitalOcean Toronto VPS
If Brume 3 or residential ISP is unavailable, failover to a cloud VPS in the same region.
```
DigitalOcean Droplet (Toronto) — $5 USD/month
├── Ubuntu Server 24.04
├── WireGuard server
└── Canadian datacenter IP (fallback)
```

Failover steps:
1. Provision $5 Ubuntu droplet in Toronto region
2. Install WireGuard server
3. Add as second WireGuard profile on Beryl 7
4. Switch profiles manually when needed

---

## Checklist
- [ ] Connect Brume 3 WAN to ISP router LAN port
- [ ] Configure DuckDNS dynamic DNS on Brume 3
- [ ] Enable WireGuard server on Brume 3
- [ ] Set port forwarding on ISP router (UDP 51820 → Brume 3)
- [ ] Configure Beryl 7 WireGuard client → Brume 3 tunnel
- [ ] Enable kill switch on Beryl 7
- [ ] Verify residential IP from remote location
- [ ] Add both routers to GoodCloud for remote monitoring
- [ ] Test failover to DigitalOcean Toronto VPS

---

## Verification
```bash
# From laptop behind Beryl 7 with Brume 3 tunnel active
# Should return residential IP of host location
curl ifconfig.me

# Verify geolocation shows correct country/region
curl ipinfo.io
```

---

## Key Decisions
- **Brume 3 as server, Beryl 7 as client** — traffic must exit through the residential location, so the server must be at that location and the client connects to it from the remote end
- **DuckDNS on Brume 3** — residential ISPs assign dynamic IPs; DuckDNS ensures the Beryl 7 always finds the Brume 3 regardless of IP changes
- **Kill switch on Beryl 7** — prevents accidental IP leaks if the tunnel drops unexpectedly
- **DigitalOcean failover** — provides redundancy if the residential location has downtime; datacenter IP is less ideal but functional as a backup

---

## Lessons Learned
- Port forwarding availability varies by ISP — verify before committing to this architecture
- Residential IPs can occasionally be flagged by services — datacenter IPs are more consistent but less convincing as residential
- GoodCloud allows remote rebooting of both GL-inet devices without needing SSH access — useful for non-technical host locations

---

*[← Stage 4](stage-04-beryl7.md) | [Back to README](../README.md) | [→ Stage 6](stage-06-opnsense.md)*
