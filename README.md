<div align="center">

# GKI Kernel Builder

[![Android](https://img.shields.io/badge/Android-16-blue)](https://android.googlesource.com/)
[![Linux](https://img.shields.io/badge/Kernel-6.12.30-red)](https://kernel.org/)
[![Root](https://img.shields.io/badge/Root-SukiSU--Nova-green)](https://github.com/SukiSU-Nova/SukiSU-Nova)

Custom Android 16 GKI kernel (`6.12.30-android16`, `2025-07`) with **SukiSU-Nova**, **SUSFS v2.4.0**, **NoMount**, **DroidSpaces**, **USB Arsenal**, and **Kali NetHunter**.

</div>

---

## ✨ Key Features

- 🔐 **Root & KPM**: **SukiSU-Nova** with built-in NyaZygisk, KPM (`CONFIG_KPM=y`), single-key manager verification, and bundled `arm64-v8a` Manager APK.
- 🛡️ **Stealth & Root Hiding**: Built-in **SUSFS v2.4.0**, **NoMount v2.3.1** VFS redirection, sanitized `/proc/config.gz`, stock `kleaf@build-host` metadata, Scoped-Storage Unicode Guard, and **Baseband Guard (BBG)**.
- 🐉 **USB Arsenal & Wireless Stack**: Built-in BadUSB HID (`/dev/hidg1` keyboard, `/dev/hidg2` mouse, custom `bInterval`), PiKVM DVD-ROM emulation (>2.36 GB ISOs), plus modular (`=m`) USB Wi-Fi, Gigabit Ethernet, Serial, and Bluetooth drivers.
- 📦 **DroidSpaces Containers**: Full container runtime support with SYSVIPC and cgroup v2 CPU/process limits (`CONFIG_CFS_BANDWIDTH=y`, `CONFIG_CGROUP_PIDS=y`).
- 🚀 **Performance & Networking**: Mainline BBR (default), CAKE Qdisc, WireGuard, IP Set, CIFS/SMB, NTSync, MGLRU (`0x0007`), eBPF/BTF, and FUSE-BPF.
- ⚡ **Vendor Module Bypass**: Built-in `bad_version` bypass so stock OEM display, touchscreen, Wi-Fi, and modem drivers load cleanly on boot.

---

## 📡 Supported Hardware & Drivers

<details>
<summary><b>Supported USB Wi-Fi Adapters (Monitor Mode & Frame Injection)</b></summary>
<br>

| Vendor | Driver | Popular Tested Adapters | Capabilities |
| :--- | :--- | :--- | :--- |
| **MediaTek** | `mt76x2u` / `mt76x0u` | **Alfa AWUS036ACM** (MT7612U), **Alfa AWUS036ACHM** (MT7610U), Archer T2U Plus v1, Netgear A6210 | 2.4/5 GHz 802.11ac, Monitor, Injection, AP |
| **MediaTek** | `mt7601u` | Generic MT7601U Mini Dongles, TP-Link TL-WN727N v5 | 2.4 GHz 802.11n, Monitor, Injection |
| **Atheros** | `ath9k_htc` | **TP-Link TL-WN722N v1** (AR9271), **Alfa AWUS036NHA** | 2.4 GHz 802.11n, Monitor, Injection, AP |
| **Atheros** | `carl9170` | TP-Link TL-WN821N v2, D-Link DWA-160 vA1/vA2 (AR9170) | 2.4/5 GHz 802.11n, Monitor, Injection, AP |
| **Ralink** | `rt2800usb` | **Alfa AWUS036NH**, **Alfa AWUS036NEH**, Panda PAU05/PAU06/PAU09 (RT3070/RT5370/RT5572) | 2.4/5 GHz 802.11n, Monitor, Injection, AP |
| **Realtek** | `rtw88` | Edimax EW-7822ULC (RTL8822BU), Archer T2U Nano/Plus v2 (RTL8821CU), Comfast CF-924AC v2 (RTL8822CU) | 2.4/5 GHz 802.11ac, Monitor, Injection |
| **Realtek** | `rtl8xxxu` | TP-Link TL-WN725N v2/v3 (RTL8188EUS), TL-WN823N (RTL8192EU) | 2.4 GHz 802.11n, Monitor |

</details>

<details>
<summary><b>USB Gadgets, Ethernet, Serial & WebUI Dashboard</b></summary>
<br>

- 🦆 **BadUSB & USB Arsenal (Built-in)**: Multi-gadget ConfigFS, HID keyboard/mouse, >2.36 GB ISO mass storage, and USB NCM/ECM/RNDIS tethering NAT.
- 🌐 **USB Ethernet**: Realtek RTL8152/RTL8153 (`r8152`), ASIX AX88179 (`ax88179_178a`), CDC-ECM, and CDC-NCM.
- 🔌 **USB Serial & Bluetooth**: FTDI, CH341, CP210X, PL2303, CDC-ACM, and external USB Bluetooth (`btusb` + RFCOMM/BNEP/HIDP).
- 📱 **NetHunter WebUI**: Built into `Nethunter-Wireless-Modules.zip` (open via the **WebUI** button in SukiSU-Nova Manager) to control TCP congestion, load/unload `.ko` drivers on demand, lock MGLRU (`0x0007`), and view live logs.

</details>

> [!TIP]
> **Internal Wi-Fi (`wlan0`) WPS / PixieDust Tip:** Turn on your **Mobile Hotspot** before running PixieDust/WPS tools (e.g., Stryker, Oneshot) on `wlan0` so the OEM driver does not power down the interface when Wi-Fi is toggled off.

---

## 📲 Installation

1. **Extract Bundle**: Download `*-Bundle.zip` from Releases and extract it.
2. **Flash Kernel**: Flash `*-AnyKernel3.zip` via **[Kernel Flasher](https://github.com/fatalcoder524/KernelFlasher/releases)**, custom recovery, or **SukiSU-Nova Manager** *(select **KPM Operation → KPM Patch** in SukiSU-Nova Manager if you want KPM active on boot)*.
3. **Install Manager**: Install `SukiSU_Nova_*-arm64-v8a-release.apk` and reboot.
4. **Configure SUSFS**: Open **SukiSU-Nova Manager → Extension features → SuSFS** to configure root hiding and toggle **Auto-Start** *(keep "Cleanup Residue" off if you use Stryker)*.
5. **Optional Modules** *(flash inside SukiSU-Nova Manager)*:
   - `NoMount-*.zip` — Stealth VFS module mounting.
   - `Nethunter-Wireless-Modules.zip` — External USB Wi-Fi/Ethernet/Serial/Bluetooth drivers, firmware, and WebUI.

---

## 📱 Tested Device

- **Device**: Redmi Note 14 4G (`tanzanite` / MediaTek Helio G99)
- **OS**: Xiaomi HyperOS 3 (Android 16, `6.12.30-android16`)

---

## 🏆 Credits

- [WildKernels/GKI_KernelSU_SUSFS](https://github.com/WildKernels/GKI_KernelSU_SUSFS) · [SukiSU-Nova](https://github.com/SukiSU-Nova/SukiSU-Nova) · [simonpunk/susfs4ksu](https://gitlab.com/simonpunk/susfs4ksu) · [maxsteeel/nomount](https://github.com/maxsteeel/nomount) · [vc-teahouse/Baseband-guard](https://github.com/vc-teahouse/Baseband-guard) · [ravindu644/Droidspaces-OSS](https://github.com/ravindu644/Droidspaces-OSS) · [ravindu644/USB-Arsenal](https://github.com/ravindu644/USB-Arsenal) · [Kali NetHunter](https://www.kali.org/docs/nethunter/) · [Kernel Flasher](https://github.com/fatalcoder524/KernelFlasher)
