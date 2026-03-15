# UFW Firewall Rules

## Host: M710q homelab (192.168.178.64)
## OS: Ubuntu Server 24.04 LTS

---

## Default Policies
```bash
sudo ufw default deny incoming
sudo ufw default allow outgoing
```

## Open Ports

| Port | Protocol | Service | Notes |
|------|----------|---------|-------|
| 22 | TCP | SSH | Remote management |
| 53 | TCP/UDP | Pi-hole DNS | Network-wide DNS resolver |
| 80 | TCP | Pi-hole Admin | Web dashboard |
| 443 | TCP | HTTPS | Future services |
| 51820 | UDP | WireGuard | VPN server |
| 5900 | TCP | VNC | Temporary — open only during VM console access |
| 6080 | TCP | noVNC | Temporary — open only during VM console access |

## Applied Rules
```bash
sudo ufw allow 22/tcp
sudo ufw allow 53/tcp
sudo ufw allow 53/udp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw allow 51820/udp
sudo ufw enable
```

## Temporary Rules (open/close as needed)
```bash
# Open for VM console access
sudo ufw allow 5900/tcp
sudo ufw allow 6080/tcp

# Close when done
sudo ufw delete allow 5900/tcp
sudo ufw delete allow 6080/tcp
```

## Forward Policy
Required for WireGuard NAT:
```bash
# /etc/default/ufw
DEFAULT_FORWARD_POLICY="ACCEPT"
```

## NAT Rules for WireGuard
```bash
# /etc/ufw/before.rules — add before *filter section
*nat
:POSTROUTING ACCEPT [0:0]
-A POSTROUTING -s 10.0.0.0/24 -o br0 -j MASQUERADE
COMMIT
```

## Verify
```bash
sudo ufw status verbose
sudo iptables -t nat -L -n -v
```

---

## Notes
- Port 5900/6080 are for VM console access only — always close after use
- br0 replaced enp0s31f6 as the outbound interface after Linux bridge configuration (Stage 6)
- Pi-hole uses host networking — ports 53 and 80 are bound directly on the host
