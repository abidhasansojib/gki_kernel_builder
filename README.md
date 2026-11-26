<div align="center">

# GKI Kernel Builder

[![Android](https://img.shields.io/badge/Android-16-blue)](https://android.googlesource.com/)
[![Linux](https://img.shields.io/badge/Kernel-6.12.30-red)](https://kernel.org/)
[![Root](https://img.shields.io/badge/Root-SukiSU--Nova-green)](https://github.com/SukiSU-Nova/SukiSU-Nova)

Android 16 GKI kernel (`6.12.30-android16`, `2025-07`) with SukiSU-Nova, SUSFS, NoMount, DroidSpaces, and NetHunter wireless support.

</div>

---

## Features

- **SukiSU-Nova** — Kernel-based root with built-in Zygisk and KPM support
- **SUSFS & NoMount** — Root hiding and stealth module mounting
- **Kali NetHunter** — External USB Wi-Fi (monitor mode & injection), Ethernet, Serial, and Bluetooth drivers with WebUI
- **USB Arsenal** — Boot ISO images (>2.36 GB), BadUSB keyboard/mouse emulation, and USB tethering
- **DroidSpaces** — Linux container runtime support
- **Baseband Guard** — Protects modem and radio partitions
- **Networking** — WireGuard, BBR, CAKE Qdisc, IPSet, and CIFS/SMB
- **Performance** — NTSync, MGLRU, eBPF/BTF, and memory/scheduler tuning

---

## Supported Wi-Fi Adapters

<details>
<summary><b>View Supported USB Wi-Fi Adapters</b></summary>
<br>

| Vendor | Driver | Supported Adapters | Capabilities |
| :--- | :--- | :--- | :--- |
| **MediaTek** | `mt76x2u` / `mt76x0u` | Alfa AWUS036ACM (MT7612U), Alfa AWUS036ACHM (MT7610U), Archer T2U Plus v1, Netgear A6210 | 2.4/5 GHz 802.11ac, Monitor, Injection, AP |
| **MediaTek** | `mt7601u` | Generic MT7601U, TP-Link TL-WN727N v5 | 2.4 GHz 802.11n, Monitor, Injection |
| **Atheros** | `ath9k_htc` | TP-Link TL-WN722N v1 (AR9271), Alfa AWUS036NHA | 2.4 GHz 802.11n, Monitor, Injection, AP |
| **Atheros** | `carl9170` | TP-Link TL-WN821N v2, D-Link DWA-160 vA1/vA2 (AR9170) | 2.4/5 GHz 802.11n, Monitor, Injection, AP |
| **Ralink** | `rt2800usb` | Alfa AWUS036NH, Alfa AWUS036NEH, Panda PAU05/PAU06/PAU09 (RT3070/RT5370/RT5572) | 2.4/5 GHz 802.11n, Monitor, Injection, AP |
| **Realtek** | `rtw88` | Edimax EW-7822ULC (RTL8822BU), Archer T2U Nano/Plus v2 (RTL8821CU), Comfast CF-924AC v2 (RTL8822CU) | 2.4/5 GHz 802.11ac, Monitor, Injection |
| **Realtek** | `rtl8xxxu` | TP-Link TL-WN725N v2/v3 (RTL8188EUS), TL-WN823N (RTL8192EU) | 2.4 GHz 802.11n, Monitor |

</details>

---

## Installation

1. Download and extract `*-Bundle.zip` from Releases.
2. Flash `*-AnyKernel3.zip` via [Kernel Flasher](https://github.com/fatalcoder524/KernelFlasher/releases), recovery, or SukiSU-Nova Manager *(use **KPM Operation → KPM Patch** to enable KPM on boot)*.
3. Install `SukiSU_Nova_*-arm64-v8a-release.apk` and reboot.
4. Configure root hiding in **SukiSU-Nova Manager → Extension features → SuSFS** and enable **Auto-Start**.
5. *(Optional)* Flash `NoMount-*.zip` and `Nethunter-Wireless-Modules.zip` in SukiSU-Nova Manager.
