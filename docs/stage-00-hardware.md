# Stage 0 — Hardware Acquisition & Assessment

## Goal
Source a refurbished Lenovo ThinkCentre M710q Tiny, verify internals, document maximum upgrade path.

## Skills Developed
Hardware identification, DDR4 rank matching, NVMe compatibility, server form-factor planning.

---

## Hardware Specs

| Component | Spec |
|-----------|------|
| **Machine** | Lenovo ThinkCentre M710q Tiny |
| **CPU** | Intel i5-6500T — 4 cores/4 threads, 2.5GHz/3.1GHz, 6MB cache, HD 530 |
| **RAM** | 16GB (2x8GB) Samsung/Hynix DDR4-2400 SO-DIMM CL17 |
| **Storage (OS)** | 250GB NVMe M.2 Samsung 970 EVO Plus |
| **Storage (Data)** | 128GB SATA SSD LiteOn (`/mnt/storage`) |
| **Network** | 1x Intel I219-LM Gigabit LAN |
| **Ports** | 6x USB 3.1, 1x COM DB-9, 2x DisplayPort, 1x LAN |
| **Power** | Original Lenovo 65W adapter |

## Maximum Hardware Ceiling

| Component | Current | Maximum |
|-----------|---------|---------|
| **CPU** | Intel i5-6500T — 4 cores/4 threads, 2.5GHz/3.1GHz, 6MB cache, HD 530, DDR4-2133 native | i7-7700T (4C/8T, 2.9/3.8GHz, 8MB cache, DDR4-2400) |
| **RAM** | 16GB DDR4-2400 | 32GB (2x16GB DDR4-2400) |
| **NVMe** | 250GB PCIe 3.0 x4 | Up to 2TB PCIe 3.0 x4 |
| **SATA** | 128GB 2.5" SSD | 2.5" SSD/HDD via expansion chassis |

## Planned Upgrades
- [ ] CPU: Upgrade to Intel i7-7700T (pending thermal paste + inspection)
- [ ] RAM: Upgrade to 32GB when VM workloads demand it
- [ ] Managed switch: TP-Link TL-SG608E 8-Port Gigabit (ordered)
- [ ] USB 3.0 to Ethernet adapter: for WAN/LAN architecture


---

## Checklist
- [x] Source refurbished M710q Tiny
- [x] Verify internals: RAM rank (1Rx8), M.2 slot, expansion chassis
- [x] Upgrade RAM to 16GB (matched Hynix 1Rx8 DDR4-2400)
- [x] Install 250GB NVMe SSD (Samsung 970 EVO Plus)
- [x] Document maximum upgrade path

---

## Key Decisions
- Chose M710q Tiny over tower form factor for low power consumption (~35W TDP CPU) and compact footprint
- Verified DDR4 rank matching (1Rx8) before purchasing RAM to avoid compatibility issues
- Selected Samsung 970 EVO Plus NVMe for OS — reliable, well-supported under Linux
- Retained 128GB SATA SSD as secondary storage for Docker volumes and VM disks

---

*[← Back to README](../README.md) | [→ Stage 1](stage-01-linux.md)*
