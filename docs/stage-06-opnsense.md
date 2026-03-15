# Stage 6 — Firewall Lab (OPNsense VM)

## Goal
Deploy OPNsense 25.1 in a KVM/QEMU VM. Build firewall rule sets, NAT, and VLANs. Promote to full network gateway with USB NIC and managed switch.

## Skills Developed
VM management (KVM/QEMU/libvirt), Linux bridge networking, firewall rule logic, NAT, VLAN theory, DMZ architecture.

**Security+ relevance:** Stateful vs stateless firewalls, DMZ, network segmentation, IDS/IPS integration, network access control

---

## Architecture
```
Internet → Upstream Router (192.168.178.1)
                ↓
         M710q Ubuntu Server
         ├── br0 (Linux bridge — 192.168.178.64)
         │   ├── enp0s31f6 (physical NIC)
         │   └── vnet0 (OPNsense VM virtual NIC)
         ├── OPNsense VM (192.168.178.72)
         │   └── WAN: vtnet0 via br0
         └── WireGuard (10.0.0.1)
```

> **Current state:** OPNsense running in learning mode with single NIC (WAN only). USB NIC pending arrival to enable proper WAN/LAN separation and promote OPNsense to full network gateway.

---

## Why OPNsense over pfSense

| | OPNsense | pfSense |
|--|----------|---------|
| **License** | BSD open source | BSL (restricted) |
| **UI** | Modern, clean | Dated |
| **Updates** | Frequent | Slower |
| **API** | REST API built-in | Limited |
| **Community** | Active | Large but fragmented |

---

## Pre-requisites

### Verify KVM Support
```bash
egrep -c '(vmx|svm)' /proc/cpuinfo
# Returns 8 on i5-6500T (4 cores × 2 hyperthreading) — KVM supported
```

### Install KVM/QEMU/libvirt
```bash
sudo apt install -y qemu-kvm libvirt-daemon-system libvirt-clients \
  bridge-utils virtinst virt-manager

sudo usermod -aG libvirt cyberphil
sudo usermod -aG kvm cyberphil
sudo systemctl enable --now libvirtd
```

### Disable libvirt Default Network
Conflicts with Pi-hole on port 53:
```bash
sudo virsh net-destroy default
sudo virsh net-autostart --disable default
sudo systemctl restart libvirtd
```

---

## Linux Bridge Configuration

Required to allow host ↔ VM communication and replace macvtap (which isolates host from VM).

### `/etc/netplan/50-cloud-init.yaml`
```yaml
network:
  version: 2
  ethernets:
    enp0s31f6:
      dhcp4: no
  bridges:
    br0:
      interfaces: [enp0s31f6]
      dhcp4: no
      addresses: [192.168.178.64/24]
      routes:
        - to: default
          via: 192.168.178.1
      nameservers:
        addresses: [127.0.0.1, 208.67.222.222]
      parameters:
        stp: false
        forward-delay: 0
```
```bash
sudo netplan apply
```

> **Note:** After bridge configuration, WireGuard PostUp/PostDown must reference `br0` instead of `enp0s31f6`.

### Update WireGuard for br0
```bash
# /etc/wireguard/wg0.conf
PostUp = iptables -A FORWARD -i wg0 -j ACCEPT; iptables -A FORWARD -o wg0 -j ACCEPT; iptables -t nat -A POSTROUTING -o br0 -j MASQUERADE
PostDown = iptables -D FORWARD -i wg0 -j ACCEPT; iptables -D FORWARD -o wg0 -j ACCEPT; iptables -t nat -D POSTROUTING -o br0 -j MASQUERADE
```
```bash
sudo systemctl restart wg-quick@wg0
```

---

## OPNsense ISO Download
```bash
cd /mnt/storage/isos
sudo wget https://mirror.ams1.nl.leaseweb.net/opnsense/releases/25.1/OPNsense-25.1-dvd-amd64.iso.bz2
sudo bzip2 -d OPNsense-25.1-dvd-amd64.iso.bz2
ls -lh OPNsense-25.1-dvd-amd64.iso
# 2.1G
```

---

## VM Creation
```bash
sudo virt-install \
  --name opnsense \
  --ram 4096 \
  --vcpus 2 \
  --os-variant freebsd13.0 \
  --machine q35 \
  --disk path=/mnt/storage/opnsense.qcow2,size=16,format=qcow2,bus=sata \
  --cdrom /mnt/storage/isos/OPNsense-25.1-dvd-amd64.iso \
  --network none \
  --graphics vnc,listen=0.0.0.0,port=5900 \
  --noautoconsole \
  --events on_reboot=restart
```

> **Key flags:**
> - `--machine q35` — better FreeBSD/OPNsense compatibility than default i440fx
> - `bus=sata` — avoids vm_fault pager errors caused by virtio-blk on FreeBSD
> - `--network none` — install without network to avoid macvtap issues; attach bridge after install
> - `--events on_reboot=restart` — allows VM to restart naturally after install

---

## Installation Process

### noVNC Access
```bash
sudo apt install -y novnc
sudo ufw allow 6080/tcp
sudo websockify -D --web=/usr/share/novnc/ 6080 localhost:5900
```

Access via WireGuard tunnel: `http://10.0.0.1:6080/vnc.html`

### Installer Steps
1. Login: `installer` / `opnsense`
2. Keymap: default
3. Install (UFS) — simpler, lower overhead than ZFS for a VM
4. Select disk: `ada0` (16GB virtual disk)
5. Set root password
6. **Select "Halt" instead of "Reboot"**

### Critical: Halt Instead of Reboot
```bash
# After installer halts the VM, start it cleanly
# ISO is automatically detached on halt + restart
sudo virsh start opnsense
```

> **Important:** Selecting "Reboot" in the installer causes vm_fault pager errors on first boot. Always halt, then start manually via virsh.

---

## Post-Install Network Attachment
```bash
# Attach bridge interface after successful install
sudo virsh attach-interface opnsense \
  --type bridge \
  --source br0 \
  --model virtio \
  --config

sudo virsh reboot opnsense
```

---

## OPNsense Initial Configuration

### Assign Interface
Console menu → Option 1 (Assign interfaces):
- VLANs: No
- LAGGs: No
- WAN: `vtnet0`
- LAN: (skip — single NIC for now)

### Set WAN IP via DHCP
Console menu → Option 2 (Set interface IP):
- Interface: vtnet0
- Configure via DHCP: Yes
- IP assigned: `192.168.178.72`

Reserve IP on router for OPNsense MAC address.

### Web UI Access
```
https://192.168.178.72
```

Via WireGuard tunnel — requires `192.168.178.0/24` in client `AllowedIPs`.

Default credentials:
- Username: `root`
- Password: (set during install)

---

## VM Management Commands
```bash
# Status
sudo virsh list --all

# Start/stop
sudo virsh start opnsense
sudo virsh shutdown opnsense
sudo virsh destroy opnsense  # force stop

# Check network interfaces
sudo virsh domiflist opnsense

# Check disk
sudo virsh domblklist opnsense

# Reduce RAM after stable (optional)
sudo virsh setmaxmem opnsense 1024 --config
sudo virsh setmem opnsense 1024 --config
```

---

## Checklist
- [x] Install KVM/QEMU/libvirt on Ubuntu Server
- [x] Disable libvirt default network (Pi-hole port 53 conflict)
- [x] Configure Linux bridge (br0) replacing macvtap
- [x] Update WireGuard PostUp/PostDown for br0
- [x] Download OPNsense 25.1 ISO
- [x] Deploy OPNsense VM (q35, SATA, 4GB RAM, 16GB disk)
- [x] Complete OPNsense installer (UFS, halt method)
- [x] Attach bridge interface post-install
- [x] Assign WAN interface (vtnet0)
- [x] OPNsense accessible at 192.168.178.72
- [x] OPNsense accessible via WireGuard tunnel
- [x] Reserve 192.168.178.72 on router
- [x] Take Timeshift snapshot: Stage 6 complete
- [ ] Install USB NIC (second NIC for WAN/LAN separation)
- [ ] Install TP-Link TL-SG608E managed switch
- [ ] Build allow/deny firewall rule sets
- [ ] Configure NAT rules
- [ ] Configure VLANs and inter-VLAN routing
- [ ] Promote OPNsense to full network gateway
- [ ] Document IDS/IPS integration options

---

## Troubleshooting

### vm_fault pager read error on boot
FreeBSD panics with virtio-blk disk driver on some KVM configurations.
**Fix:** Use `bus=sata` and `--machine q35` in virt-install. Use halt + manual start instead of reboot.

### libvirt dnsmasq conflicts with Pi-hole
libvirt's default NAT network spawns dnsmasq on port 53.
**Fix:** Destroy and disable autostart on libvirt default network before starting Pi-hole.

### Host cannot ping OPNsense VM
macvtap mode isolates VM from host by design.
**Fix:** Replace macvtap with Linux bridge (br0). Host can then reach VM via bridge.

### OPNsense not reachable via WireGuard
WireGuard client `AllowedIPs` must include `192.168.178.0/24` to route LAN traffic through the tunnel.
**Fix:** Update client config: `AllowedIPs = 10.0.0.0/24, 192.168.178.0/24`

### WireGuard loses internet after bridge config
WireGuard PostUp/PostDown referenced `enp0s31f6` which no longer has an IP after bridge setup.
**Fix:** Update PostUp/PostDown to reference `br0` instead of `enp0s31f6`.

---

## Key Decisions
- **OPNsense over pfSense** — open source license, modern UI, built-in REST API, more frequent updates
- **q35 machine type** — better PCIe/SATA support for FreeBSD vs legacy i440fx
- **SATA bus over virtio-blk** — FreeBSD has known issues with virtio-blk on certain KVM versions; SATA is more compatible
- **Linux bridge over macvtap** — macvtap prevents host ↔ VM communication; bridge enables full connectivity
- **Halt instead of reboot** — clean power cycle avoids vm_fault pager errors on first boot from installed disk
- **Single NIC initially** — USB NIC not yet available; OPNsense runs in learning mode until proper WAN/LAN separation is possible

---

## Lessons Learned
- FreeBSD (OPNsense) is more sensitive to virtual hardware compatibility than Linux VMs — machine type and disk bus matter significantly
- libvirt spawns dnsmasq even for networks defined without DHCP — must fully disable default network to avoid port 53 conflicts
- The Linux bridge MAC address differs from the physical NIC MAC — DHCP reservations must be updated to the bridge MAC or use static IP in netplan
- noVNC through WireGuard tunnel bypasses Windows firewall restrictions that block direct VNC connections

---

*[← Stage 5](stage-05-exitnode.md) | [Back to README](../README.md) | [→ Stage 7](stage-07-freeswitch.md)*
