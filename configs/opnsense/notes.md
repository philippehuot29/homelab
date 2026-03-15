# OPNsense VM — Configuration Notes

## Instance Details

| Setting | Value |
|---------|-------|
| **Version** | OPNsense 25.1 (amd64) |
| **VM Name** | opnsense |
| **Host** | M710q (192.168.178.64) |
| **Hypervisor** | KVM/QEMU via libvirt |
| **Machine type** | q35 |
| **Disk** | 16GB qcow2, SATA bus (`/mnt/storage/opnsense.qcow2`) |
| **RAM** | 4GB allocated (reducible to 1GB post-stabilization) |
| **vCPUs** | 2 |
| **Network** | vtnet0 via Linux bridge br0 |
| **WAN IP** | 192.168.178.72 (reserved on router) |
| **Web UI** | https://192.168.178.72 |

---

## Current State
- WAN interface assigned (vtnet0)
- DHCP on WAN — IP reserved at 192.168.178.72
- Web UI accessible via WireGuard tunnel
- Running in learning mode — single NIC, no LAN separation yet

---

## Pending (hardware arrival)
- [ ] Install USB 3.0 to Gigabit adapter (second NIC)
- [ ] Attach second NIC to OPNsense as LAN interface
- [ ] Install TP-Link TL-SG608E managed switch
- [ ] Configure VLANs on switch
- [ ] Build firewall allow/deny rule sets
- [ ] Configure NAT rules
- [ ] Configure inter-VLAN routing
- [ ] Promote OPNsense to full network gateway

---

## VM Management Quick Reference
```bash
# Status
sudo virsh list --all

# Start / shutdown / force stop
sudo virsh start opnsense
sudo virsh shutdown opnsense
sudo virsh destroy opnsense

# Console access (serial)
sudo virsh console opnsense
# Exit: Ctrl + ]

# Network interfaces
sudo virsh domiflist opnsense

# Disk list
sudo virsh domblklist opnsense

# Eject ISO
sudo virsh change-media opnsense sdb --eject --force

# Reduce RAM (after stable)
sudo virsh setmaxmem opnsense 1024 --config
sudo virsh setmem opnsense 1024 --config
```

---

## noVNC Access
```bash
# Start noVNC (open temporarily for console access)
sudo ufw allow 6080/tcp
sudo websockify -D --web=/usr/share/novnc/ 6080 localhost:5900

# Access via WireGuard tunnel
# http://10.0.0.1:6080/vnc.html

# Close when done
sudo ufw delete allow 6080/tcp
sudo ufw delete allow 5900/tcp
```

---

## Firewall Rule Planning (pending hardware)

### Planned Zones
| Zone | Interface | Subnet | Purpose |
|------|-----------|--------|---------|
| WAN | vtnet0 | DHCP | Upstream internet |
| LAN | vtnet1 (USB NIC) | 10.10.0.0/24 | Trusted devices |
| MGMT | VLAN10 | 10.10.10.0/24 | Homelab management |
| IOT | VLAN20 | 10.10.20.0/24 | Isolated IoT devices |

### Planned Rule Sets
- LAN → WAN: allow established, deny by default
- MGMT → all zones: allow (admin access)
- IOT → internet only: deny LAN/MGMT access
- WAN → all: deny (stateful firewall default)

---

## Known Issues & Fixes

| Issue | Cause | Fix |
|-------|-------|-----|
| vm_fault pager read error | virtio-blk incompatibility with FreeBSD | Use `bus=sata` + `--machine q35` |
| Host cannot reach VM | macvtap isolation | Replace macvtap with Linux bridge (br0) |
| WireGuard no internet after bridge | PostUp referenced wrong interface | Update PostUp/PostDown to use `br0` |
| OPNsense not reachable via WireGuard | AllowedIPs missing LAN subnet | Add `192.168.178.0/24` to client AllowedIPs |
| libvirt dnsmasq conflicts Pi-hole | Both bind port 53 | Disable libvirt default network |
