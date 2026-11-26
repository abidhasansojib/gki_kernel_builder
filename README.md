<div align="center">

# GKI Kernel Builder

[![Android](https://img.shields.io/badge/Android-16-blue)](https://android.googlesource.com/)
[![Linux](https://img.shields.io/badge/Kernel-6.12.30-red)](https://kernel.org/)
[![Root](https://img.shields.io/badge/Root-SukiSU--Nova-green)](https://github.com/SukiSU-Nova/SukiSU-Nova)

Android 16 GKI kernel (`6.12.30-android16`, `2025-07`) with SukiSU-Nova, SUSFS, NoMount, DroidSpaces, and NetHunter wireless support.

</div>

---

## Features

- **Root**: SukiSU-Nova with built-in NyaZygisk, KPM (`CONFIG_KPM=y`), and single-key manager verification.
- **Stealth**: SUSFS v2.4.0, NoMount v2.3.1 VFS redirection, sanitized `/proc/config.gz`, stock `kleaf@build-host` metadata, Scoped-Storage Unicode Guard, and Baseband Guard.
- **Wireless & USB Gadgets**: Built-in BadUSB HID (`/dev/hidg1`, `/dev/hidg2`), PiKVM DVD-ROM emulation (>2.36 GB ISOs), USB NCM/ECM/RNDIS tethering, and modular (`=m`) USB Wi-Fi, Ethernet, Serial, and Bluetooth drivers with a Material 3 WebUI.
- **Containers**: DroidSpaces runtime support (`CONFIG_SYSVIPC=y`, `CONFIG_CFS_BANDWIDTH=y`, `CONFIG_CGROUP_PIDS=y`).
- **Networking & Performance**: Mainline BBR, CAKE Qdisc, WireGuard, IP Set, CIFS/SMB, NTSync, MGLRU (`0x0007`), eBPF/BTF, and FUSE-BPF.
- **Compatibility**: Built-in vendor module version bypass (`bad_version`).

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

---

## Credits

- [SukiSU-Nova](https://github.com/SukiSU-Nova/SukiSU-Nova)
- [SUSFS](https://gitlab.com/simonpunk/susfs4ksu)
- [NoMount](https://github.com/maxsteeel/nomount)
- [WildKernels](https://github.com/WildKernels/GKI_KernelSU_SUSFS)
