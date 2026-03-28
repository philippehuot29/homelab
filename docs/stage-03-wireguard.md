# Stage 3 — VPN Server (WireGuard)

## Goal
Self-hosted WireGuard VPN server on M710q, accessible from anywhere. Eliminate reliance on commercial VPN providers.

## Skills Developed
VPN fundamentals, asymmetric key cryptography, tunnel configuration, firewall rules, NAT traversal, dynamic DNS.

**Security+ relevance:** Tunneling protocols, IPSec vs WireGuard vs OpenVPN comparison, encryption key management, remote access security

---

## Architecture
```
Laptop/Mobile (WireGuard client)
        ↓
philippehuot29.duckdns.org:51820
        ↓
M710q WireGuard Server (10.0.0.1)
        ↓
Home Network / Internet
```

WireGuard runs as a **kernel module** — no Docker needed. Lower overhead, faster performance, and more stable than userspace VPN implementations.

---

## Why WireGuard over OpenVPN/IPSec

| | WireGuard | OpenVPN | IPSec |
|--|-----------|---------|-------|
| **Code size** | ~4,000 lines | ~600,000 lines | Complex |
| **Performance** | Excellent | Good | Good |
| **Setup complexity** | Low | High | High |
| **Kernel integration** | Yes (5.6+) | No | Partial |
| **Handshake** | ~1ms | Seconds | Seconds |

---

## Installation
```bash
sudo apt install wireguard
```

### Generate Server Keys
```bash
wg genkey | sudo tee /etc/wireguard/server_private.key | \
wg pubkey | sudo tee /etc/wireguard/server_public.key
sudo chmod 600 /etc/wireguard/server_private.key
```

### Generate Client Keys
```bash
wg genkey | tee client_private.key | wg pubkey > client_public.key
```

---

## Configuration

### Server `/etc/wireguard/wg0.conf`
```ini
[Interface]
Address = 10.0.0.1/24
ListenPort = 51820
PrivateKey = [redacted]
PostUp = iptables -A FORWARD -i wg0 -j ACCEPT; iptables -A FORWARD -o wg0 -j ACCEPT; iptables -t nat -A POSTROUTING -o br0 -j MASQUERADE
PostDown = iptables -D FORWARD -i wg0 -j ACCEPT; iptables -D FORWARD -o wg0 -j ACCEPT; iptables -t nat -D POSTROUTING -o br0 -j MASQUERADE

[Peer]
# Laptop
PublicKey = [redacted]
AllowedIPs = 10.0.0.2/32
```

> **Note:** PostUp/PostDown reference `br0` — updated in Stage 6 when Linux bridge replaced `enp0s31f6` as the primary network interface.

### Client Config
```ini
[Interface]
Address = 10.0.0.2/24
PrivateKey = [redacted]
DNS = 10.0.0.1

[Peer]
PublicKey = [redacted]
Endpoint = philippehuot29.duckdns.org:51820
AllowedIPs = 10.0.0.0/24, 192.168.8.0/24
PersistentKeepalive = 25
```

> **AllowedIPs explanation:**
> - `10.0.0.0/24` — WireGuard tunnel subnet (reach homelab services)
> - `192.168.8.0/24` — Home LAN subnet (reach OPNsense at .72, Pi-hole at .64)
> - Omitting `0.0.0.0/0` means regular internet traffic goes direct — only homelab-bound traffic uses the tunnel

---

## UFW Rules
```bash
sudo ufw allow 51820/udp
```
```bash
# /etc/default/ufw
DEFAULT_FORWARD_POLICY="ACCEPT"
```
```bash
# /etc/ufw/before.rules — add before *filter section
*nat
:POSTROUTING ACCEPT [0:0]
-A POSTROUTING -s 10.0.0.0/24 -o br0 -j MASQUERADE
COMMIT
```

---

## Dynamic DNS (DuckDNS)

DuckDNS provides a free dynamic DNS hostname — essential since home ISPs assign dynamic public IPs.
```bash
# /etc/cron.d/duckdns — runs every 5 minutes
*/5 * * * * root curl -s "https://www.duckdns.org/update?domains=philippehuot29&token=[redacted]&ip=" > /dev/null
```

> **Security note:** Rotate your DuckDNS token periodically. Never commit the token to public repositories.

---

## Enable & Start
```bash
sudo systemctl enable wg-quick@wg0
sudo systemctl start wg-quick@wg0
sudo wg show  # verify tunnel status
```

---

## Checklist
- [x] Install WireGuard (kernel module)
- [x] Generate server and client key pairs
- [x] Configure server `wg0.conf`
- [x] Configure laptop client
- [x] Open UFW port 51820/UDP
- [x] Set `DEFAULT_FORWARD_POLICY=ACCEPT` in UFW
- [x] Take Timeshift snapshot: Stage 3 complete
- [x] Configure DuckDNS dynamic DNS (cron every 5 min)
- [x] Set port forwarding on router (UDP 51820 → 192.168.8.64)
- [x] Test connectivity from external network
- [x] Take Timeshift snapshot: Stage 3.1 complete
- [ ] Test failover to secondary tunnel

---

## Verification
```bash
# Check WireGuard interface
sudo wg show

# Check tunnel is up
ping 10.0.0.1  # from client

# Check DNS is routing through Pi-hole
dig google.com  # should show Pi-hole as resolver
```

---

## Key Decisions
- **Kernel module over Docker** — WireGuard in kernel is more stable, lower latency, and survives container restarts
- **Split tunneling** (`AllowedIPs` not `0.0.0.0/0`) — only homelab-bound traffic uses the tunnel, preserving full internet speed for regular browsing
- **DuckDNS over static IP** — home ISP assigns dynamic IPs; DuckDNS provides a stable hostname for the endpoint
- **PersistentKeepalive = 25** — keeps the tunnel alive through NAT/firewall timeouts on mobile networks

---

## Lessons Learned
- PostUp/PostDown must reference the correct outbound interface — updated from `enp0s31f6` to `br0` after Linux bridge was configured in Stage 6
- Client `AllowedIPs` controls what traffic goes through the tunnel — `0.0.0.0/0` routes everything (full VPN), specific subnets enable split tunneling
- WireGuard has no built-in dynamic DNS — DuckDNS cron job is essential for reliable remote access from dynamic IP endpoints

---

*[← Stage 2](stage-02-pihole.md) | [Back to README](../README.md) | [→ Stage 4](stage-04-beryl7.md)*
