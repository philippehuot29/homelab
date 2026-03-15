# Stage 4 — GL-inet Beryl 7 Integration

## Goal
GL-inet Beryl 7 becomes the primary network layer between devices and the upstream router. DNS forwarded to M710q Pi-hole. WireGuard kill switch enabled.

## Skills Developed
Router gateway architecture, DNS forwarding, double NAT, VPN kill switch, repeater mode for mobile use.

**Network+ relevance:** Gateway configuration, NAT, DNS forwarding, wireless networking

---

## Architecture
```
Internet → Upstream Router
                ↓
         GL-inet Beryl 7 (WAN port)
         ├── DNS → M710q Pi-hole (192.168.178.64)
         ├── VPN kill switch enabled
         └── Devices (laptop, mobile, etc.)
```

The Beryl 7 sits between devices and the upstream router, acting as a dedicated network layer with built-in VPN client, kill switch, and DNS control — without requiring any configuration on the upstream router.

---

## Why GL-inet Beryl 7

| Feature | Value |
|---------|-------|
| **OpenWrt based** | Full Linux router, SSH accessible |
| **Built-in WireGuard client** | No manual config needed |
| **VPN kill switch** | Blocks all traffic if VPN drops |
| **Repeater mode** | WiFi-as-WAN for travel/café use |
| **GoodCloud** | Remote monitoring without exposing SSH |
| **USB tethering** | Mobile data failover |

---

## Configuration Steps

### 1. Physical Setup
```
Beryl 7 WAN port → Upstream router LAN port (ethernet)
Devices → Beryl 7 (WiFi or ethernet)
```

### 2. DNS Configuration
Set Beryl 7 DNS server to M710q Pi-hole:
- Admin UI → Network → DNS
- Primary DNS: `192.168.178.64`
- All devices behind Beryl 7 automatically use Pi-hole

### 3. WireGuard Client → M710q
- Admin UI → VPN → WireGuard Client
- Import client config from Stage 3
- Enable tunnel

### 4. VPN Kill Switch
- Admin UI → VPN → VPN Dashboard
- Enable kill switch — blocks all internet traffic if WireGuard tunnel drops
- Ensures no traffic leaks outside the tunnel

### 5. SSID Configuration
- Set WiFi network name to a generic, non-identifying name
- Disable SSID broadcast optional for additional privacy

### 6. Repeater Mode (Travel)
- Admin UI → Network → WiFi → Repeater
- Connect Beryl 7 WAN to venue WiFi
- All devices behind Beryl 7 automatically protected

---

## Checklist
- [ ] Connect Beryl 7 WAN port to upstream router LAN port
- [ ] Set Beryl 7 DNS to M710q Pi-hole (192.168.178.64)
- [ ] Verify all devices behind Beryl 7 use Pi-hole
- [ ] Configure WireGuard client tunnel
- [ ] Enable VPN kill switch
- [ ] Configure SSID to generic name
- [ ] Test repeater mode (WiFi-as-WAN) at a café
- [ ] Add Beryl 7 to GoodCloud for remote monitoring

---

## Verification
```bash
# From a device behind Beryl 7
# Check DNS is using Pi-hole
nslookup google.com 192.168.178.64

# Check public IP is routing through tunnel
curl ifconfig.me

# Verify kill switch — disable WireGuard tunnel
# All internet traffic should stop immediately
```

---

## Key Decisions
- **Beryl 7 over direct router config** — upstream router (ISP-provided) has limited VPN/DNS capabilities; Beryl 7 adds a full OpenWrt layer without touching ISP equipment
- **DNS at router level** — setting DNS on Beryl 7 means all connected devices automatically use Pi-hole without per-device configuration
- **Kill switch enabled** — prevents accidental IP/DNS leaks if WireGuard tunnel drops unexpectedly

---

## GoodCloud Remote Monitoring
GoodCloud (gl-inet.com/cloud) provides a web dashboard for monitoring GL-inet devices remotely — useful for checking tunnel status and device health without exposing SSH to the internet.

---

*[← Stage 3](stage-03-wireguard.md) | [Back to README](../README.md) | [→ Stage 5](stage-05-exitnode.md)*
