<div align="center">

# 🐉 Universal Android 16 GKI NetHunter Kernel (6.12.30)
### For Redmi Note 14 4G (`tanzanite`), Xiaomi HyperOS 3.0 & All Android 16 GKI Devices

[![KernelSU](https://img.shields.io/badge/KernelSU--Next-v3.3.0-green.svg)](https://github.com/pershoot/KernelSU-Next)
[![SUSFS](https://img.shields.io/badge/SUSFS-v2.2.0-orange.svg)](https://gitlab.com/simonpunk/susfs4ksu)
[![NetHunter](https://img.shields.io/badge/Kali--NetHunter-WiFi%20Injection%20%26%20BadUSB-blueviolet.svg)](https://www.kali.org/docs/nethunter/)
[![Device](https://img.shields.io/badge/Device-Redmi%20Note%2014%204G%20(tanzanite)-teal.svg)](https://github.com/abidhasansojib/gki_kernel_builder)
[![OS](https://img.shields.io/badge/OS-Xiaomi%20HyperOS%203.0%20%7C%20Android%2016-blue.svg)](https://android.googlesource.com/)
[![Linux](https://img.shields.io/badge/Kernel-6.12.30--android16-red.svg)](https://kernel.org/)
[![NoMount](https://img.shields.io/badge/NoMount-Integrated-brightgreen.svg)](https://github.com/maxsteeel/nomount)

An advanced, automated GitHub Actions builder producing universal **Android 16 (Kernel 6.12.30, 2025-07) Generic Kernel Images (GKI)** with full **Kali NetHunter support (Wireless Packet Injection, Monitor Mode, BadUSB HID Gadget, RTL-SDR)**, multi-root implementation (**KernelSU-Next, KernelSU, ReSukiSU**), **SUSFS v2.2.0**, **NoMount VFS hooks**, **Baseband Guard (BBG)**, **DroidSpaces-OSS**, **BBRv3**, and **NTSync**.

Tested and verified on **Redmi Note 14 4G (`tanzanite`)** running **Xiaomi HyperOS 3.0.302 (Android 16)**.

</div>

---

## ⚠️ Disclaimer

I am **not responsible** for bricked devices, damaged hardware, or bootloops.
Please do thorough research and ensure you have a stock `boot.img` backup before flashing!

---

## ✨ Key Features & Capabilities

- 🐉 **Kali NetHunter Pentesting Suite**:
  - **Wireless Packet Injection & Monitor Mode**: In-tree `mac80211` and `cfg80211` frame injection support with `aircrack-ng`, `wifite`, and `mdk4`.
  - **BadUSB / HID Keyboard & Mouse Emulation**: Native USB Gadget HID support (`/dev/hidg0`) for NetHunter DuckHunter and USB Rubber Ducky payloads.
  - **38 Compiled USB WiFi & Bluetooth Drivers**: Realtek (`rtw88` 802.11ac, `rtl8xxxu`, `rtl8187`), Qualcomm/Atheros (`ath9k_htc`, `carl9170`), MediaTek (`mt7601u`, `mt76x0u`, `mt76x2u`), and Ralink (`rt2800usb`).
  - **Software Defined Radio (SDR)**: RTL2832U RTL-SDR USB dongles supported natively (`dvb_usb_rtl28xxu`).
  - **Bluetooth Frame Injection**: Generic USB Bluetooth dongles (`btusb`) with RFCOMM TTY, BNEP, and HIDP.
- 🔐 **Multi-Root Flavor Selection**:
  - **KernelSU-Next** (Recommended)
  - **KernelSU** (Official Tiann)
  - **ReSukiSU / SukiSU**
- 🛡️ **SUSFS v2.2.0**: Advanced root hiding, mount spoofing, and kernel symbol protection.
- 🪝 **NoMount Stealth VFS**: Automatic root mount isolation and stealth hooks.
- 📦 **Flashable NetHunter Wireless Module**: Automatically packages all 38 compiled `.ko` driver modules, official firmware blobs, and `insmod` scripts into a ready-to-flash `NetHunter-Wireless.zip` module.
- 🛡️ **Baseband Guard (BBG)**: LSM security module protecting critical radio and modem partitions.
- 📦 **DroidSpaces-OSS**: Lightweight namespace container runtime with SYSVIPC kABI fixes.
- 🚀 **Performance & Networking**: BBRv3 TCP congestion control, CAKE Qdisc, WireGuard, IP Set, TTL modification targets, CIFS/SMB file sharing.
- ⚡ **NTSync**: Ultra-low latency NT synchronization primitives for Windows gaming translation layers.
- 🔍 **BTF / eBPF**: BTF generation, eBPF tracing, and FUSE-BPF userspace daemon.

---

## 🐉 Supported NetHunter Hardware & WiFi Adapters

The kernel and accompanying flashable `NetHunter-Wireless.zip` module provide plug-and-play driver and firmware support for packet injection, monitor mode, AP mode, BadUSB, RTL-SDR, and Bluetooth attacks:

### 📡 Wireless WiFi Adapters (Monitor Mode & Packet Injection)

| Vendor | Supported Chipset / Driver | Popular Tested Adapters | Capabilities |
| :--- | :--- | :--- | :--- |
| **MediaTek** | `mt76x2u` / `mt76x0u` (`mt76`) | **Alfa AWUS036ACM**, **Alfa AWUS036ACHM**, TP-Link Archer T2U Plus / Nano, Netgear A6210 | Dual-band 2.4/5GHz 802.11ac, Monitor Mode, Packet Injection, AP Mode |
| **MediaTek** | `mt7601u` | Generic MT7601U Mini Dongles | 2.4GHz 802.11n, Monitor Mode, Packet Injection |
| **Atheros** | `ath9k_htc` | **TP-Link TL-WN722N v1**, **Alfa AWUS036NHA**, AR9271 | 2.4GHz 802.11n, High-power Packet Injection, AP/Master Mode |
| **Atheros** | `carl9170` | AR9170 based USB dongles | 2.4/5GHz 802.11a/b/g/n, Monitor Mode, Packet Injection |
| **Ralink** | `rt2800usb` (`rt2x00`) | **Alfa AWUS036NH**, **Alfa AWUS036NEH**, RT3070, RT2870, RT3572, RT5370 | 2.4GHz 802.11n, Long-range Packet Injection, AP Mode |
| **Realtek** | `rtw88_8822bu` / `rtw88_8822cu` | **Alfa AWUS036ACH**, **Alfa AWUS036AC**, Realtek RTL8812BU, RTL8822BU, RTL8822CU | Dual-band AC1200 / AC1300, Monitor Mode, Frame Injection |
| **Realtek** | `rtw88_8821cu` / `rtw88_8723du` | Realtek RTL8811CU, RTL8821CU, RTL8723DU | AC600 Dual-band Mini Dongles |
| **Realtek** | `rtl8xxxu` | Realtek RTL8188EUS, RTL8192EU, RTL8723AU | 2.4GHz 802.11n, Monitor Mode |
| **Realtek** | `rtl8187` | **Alfa AWUS036H** (RTL8187L) | Legacy 2.4GHz High-power Injection |

### 🛠️ Hardware Gadgets, Network Dongles & SDR

- 🦆 **BadUSB / Rubber Ducky**: Native USB HID keyboard and mouse emulation (`/dev/hidg0`) for NetHunter DuckHunter payloads.
- 📻 **Software Defined Radio (SDR)**: RTL2832U / RTL28xx based RTL-SDR USB dongles supported natively via `dvb_usb_rtl28xxu.ko` (HackRF One / Airspy supported via userspace USB OTG).
- 🌐 **USB Ethernet Adapters**: Realtek RTL8152 / RTL8153, ASIX AX88179 / AX8817x, CDC-ECM, and CDC-NCM high-speed adapters.
- 📶 **Bluetooth Attacks**: Generic USB Bluetooth dongles supported via `btusb.ko` with RFCOMM TTY and BNEP frame injection.

---

## 📱 Tested Devices & Compatibility

> [!TIP]
> **Universal GKI Compatibility**: Because this is an official Generic Kernel Image (GKI), it can be flashed on **any Android device running on kernel `6.12.30-android16`** (sublevel 30 / 2025-07 patch level).

| Device | Codename | Tested OS Version | Stock Kernel Version | Flashing Mode | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Redmi Note 14 4G** | `tanzanite` | **Xiaomi HyperOS 3.0.302** (Android 16) | `6.12.30-android16-5-g6e872b4863d6-ab13847919-4k` | **Bypass Image** (`do.flash_bypass=1`) | ✅ Fully Working |
| **Universal GKI 6.12** | `aarch64` | Android 16 (2025-07) | `6.12.30-android16` | Regular or Bypass Image | ✅ Supported |

> [!CAUTION]
> **CRITICAL COMPATIBILITY & FLASHING WARNINGS**:
> 1. **HyperOS 3.0+ Only**: Do **NOT** flash this kernel on **HyperOS < 3.0** (e.g. HyperOS 1.0 or 2.0 based on Android 14/15). Flashing an Android 16 GKI kernel on older OS versions will cause a **HARD BRICK**.
> 2. **Must Use Bypass-Image on HyperOS**: You **MUST** set `do.flash_bypass=1` in `anykernel.sh` inside the `AnyKernel3.zip` to flash `Bypass-Image`. Flashing the regular `Image` on HyperOS 3 will cause a **bootloop / soft brick** due to strict vendor module version CRC enforcement.

---

## 📋 Installation Instructions

1. **Prerequisites**:
   - Unlocked bootloader on your device (e.g., Redmi Note 14 4G `tanzanite`).
   - Backup of your current stock boot image (`boot.img`).
   - Android 16 / Xiaomi HyperOS 3.0+ installed.
   - Flashing utility (e.g. [Kernel Flasher](https://github.com/fatalcoder524/KernelFlasher) or custom recovery).

2. **Flashing Kernel (Bypass Mode for HyperOS / Tanzanite)**:
   - Download the generated `AnyKernel3.zip` artifact from the [GitHub Releases / Actions](https://github.com/abidhasansojib/gki_kernel_builder/releases).
   - Ensure `do.flash_bypass=1` is configured in `anykernel.sh` (or choose Bypass when prompted).
   - Flash the ZIP in Kernel Flasher.
   - Install the matching Manager app for your selected root implementation ([KernelSU-Next Manager](https://github.com/KernelSU-Next/KernelSU-Next/releases)).
   - Reboot device.

3. **Enabling NetHunter USB WiFi Drivers**:
   - Download the `NetHunter-Wireless.zip` module from the release.
   - Flash it in KernelSU-Next or Magisk manager.
   - Plug in your USB OTG wireless adapter (Alfa, TP-Link, MediaTek, Realtek) — the drivers and firmware will load automatically on boot.

---

## 🔍 Search & Keywords Index (SEO)

`nethunter kernel for redmi note 14 4g` · `nethunter kernel for tanzanite` · `nethunter kernel for gki 6.12` · `nethunter kernel android 16` · `redmi note 14 4g nethunter kernel` · `tanzanite nethunter kernel` · `hyperos 3.0 nethunter kernel` · `android 16 gki nethunter` · `kernelsu-next android 16 6.12` · `susfs v2.2.0 android 16` · `badusb kernel android 16` · `wifi packet injection kernel redmi note 14 4g` · `rtw88 8812bu ath9k_htc mt7612u gki 6.12`

---

## 🏆 Credits & Acknowledgments

- 🏗️ **GKI KernelSU SUSFS**: Based on work by [WildKernels](https://github.com/WildKernels/GKI_KernelSU_SUSFS)
- 🔐 **KernelSU**: Developed by [tiann](https://github.com/tiann/KernelSU)
- 🚀 **KernelSU-Next**: Developed by [rifsxd](https://github.com/KernelSU-Next/KernelSU-Next) and [pershoot](https://github.com/pershoot/KernelSU-Next)
- 🛡️ **SUSFS**: Developed by [simonpunk](https://gitlab.com/simonpunk/susfs4ksu.git)
- 🐉 **Kali NetHunter**: Developed by the [Offensive Security / Kali NetHunter Team](https://www.kali.org/docs/nethunter/)
- 🪝 **NoMount**: Developed by [maxsteeel](https://github.com/maxsteeel/nomount)
- 🛡️ **Baseband-guard**: Developed by [vc-teahouse](https://github.com/vc-teahouse/Baseband-guard)
- 📦 **DroidSpaces-OSS**: Developed by [ravindu644](https://github.com/ravindu644/Droidspaces-OSS)
- ⚡ **Kernel Flasher**: Developed by [fatalcoder524](https://github.com/fatalcoder524/KernelFlasher)
