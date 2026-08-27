<div align="center">

# GKI Kernel Builder

[![KernelSU](https://img.shields.io/badge/KernelSU--Next-Supported-green)](https://github.com/pershoot/KernelSU-Next)
[![SUSFS](https://img.shields.io/badge/SUSFS-Integrated-orange)](https://gitlab.com/simonpunk/susfs4ksu)
[![NetHunter](https://img.shields.io/badge/Kali--NetHunter-Ready-blueviolet)](https://www.kali.org/docs/nethunter/)
[![Android](https://img.shields.io/badge/Android-16-blue)](https://android.googlesource.com/)
[![Linux](https://img.shields.io/badge/Kernel-6.12.30-red)](https://kernel.org/)

An automated GitHub Actions builder for building Android 16 (Kernel 6.12.30, 2025-07) Generic Kernel Images (GKI) with multi-root flavor support (KernelSU-Next, KernelSU, ReSukiSU), SUSFS v2.2.0, NoMount VFS hooks, Kali NetHunter wireless stack & BadUSB HID gadgets, Baseband Guard, DroidSpaces-OSS, BBRv3, and NTSync.

</div>

---

## ⚠️ Disclaimer

I am **not responsible** for bricked devices, damaged hardware, or any issues that arise from using this kernel.
Please do thorough research and understand the features included before flashing!

---

## ✨ Features

- 🔐 **Multi-Root Support**: Choose between **KernelSU-Next**, **KernelSU** (tiann official), and **ReSukiSU** with automated SUSFS patch integration.
- 🛡️ **SUSFS v2.2.0**: Advanced root-hiding kernel patches and userspace integration.
- 🪝 **NoMount VFS Hooks**: Advanced VFS mounting hiding and stealth capabilities with automated hook collision avoidance.
- 🐉 **Kali NetHunter Support**:
  - **Packet Injection & Monitor Mode**: In-tree `mac80211` and `cfg80211` frame injection support.
  - **BadUSB / HID Gadgets**: USB HID Keyboard and Mouse emulation (`/dev/hidg0`) for Rubber Ducky payloads.
  - **USB WiFi Dongle Support**: Realtek (`rtw88` 802.11ac, `rtl8xxxu`, `rtl8187`), Atheros (`ath9k_htc`, `carl9170`), MediaTek (`mt7601u`, `mt76x0u`, `mt76x2u`), and Ralink (`rt2800usb`).
  - **USB Ethernet Adapters**: CDC-ECM, CDC-NCM, Realtek RTL8152, and ASIX AX88179.
  - **Bluetooth RFCOMM & SDR**: Native RFCOMM TTY and RTL-SDR (`rtl28xxu`) support.
- 📦 **Flashable NetHunter Wireless Module**: Automatically packages compiled `.ko` driver modules and official Linux firmware into a flashable KernelSU/Magisk module (`Nethunter-Wireless-Module.zip`) for plug-and-play OTG WiFi support.
- 🛡️ **Baseband Guard (BBG)**: LSM security module for critical partition write protection.
- 📦 **DroidSpaces-OSS**: Lightweight container runtime support with SYSVIPC kABI fixes.
- 🚀 **Networking & Performance**: BBRv3, CAKE Qdisc, WireGuard, IP Set, TTL targets, CIFS.
- ⚡ **NTSync**: Low-latency NT synchronization primitives.
- 🔍 **BTF / eBPF**: BTF generation, eBPF tooling, and FUSE-BPF support.

---

## 🐉 Supported NetHunter Hardware & WiFi Adapters

The kernel and accompanying flashable `Nethunter-Wireless-Module.zip` module provide plug-and-play driver and firmware support for packet injection, monitor mode, AP mode, BadUSB, RTL-SDR, and Bluetooth attacks:

### 📡 Wireless WiFi Adapters (Monitor Mode & Packet Injection)

| Vendor | Supported Chipset / Driver | Popular Tested Adapters | Capabilities |
| :--- | :--- | :--- | :--- |
| **MediaTek** | `mt76x2u` / `mt76x0u` (`mt76`) | **Alfa AWUS036ACM**, **Alfa AWUS036ACHM**, Archer T2U Plus / Nano, Netgear A6210 | Dual-band 2.4/5GHz 802.11ac, Monitor Mode, Packet Injection, AP Mode |
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
- 📻 **Software Defined Radio (SDR)**: In-kernel and USB drivers for RTL2832U / RTL-SDR (`dvb_usb_rtl28xxu`), HackRF One (`hackrf.ko`), AirSpy (`airspy.ko`), and Mirics (`msi2500.ko` / `msi001.ko`).
- 🚗 **Automotive Hacking (CARsenal)**: SocketCAN framework (`can.ko`, `can-raw.ko`, `can-bcm.ko`, `can-gw.ko`), Virtual CAN (`vcan.ko`), Serial CAN (`slcan.ko`), PEAK PCAN-USB (`peak_usb.ko`), Kvaser (`kvaser_usb.ko`), and EMS USB (`ems_usb.ko`).
- 🔌 **USB Serial & Hardware Hacking**: CDC-ACM (`cdc-acm.ko`), FTDI (`ftdi_sio.ko`), WCH (`ch341.ko`), Silicon Labs (`cp210x.ko`), and Prolific (`pl2303.ko`) for router consoles, embedded hardware debugging, and RFID cloner tools (Proxmark3 / ChameleonMini).
- 🌐 **USB Ethernet Adapters**: Realtek RTL8152 / RTL8153 (`r8152.ko`), ASIX AX88179 / AX8817x (`ax88179_178a.ko`), CDC-ECM, and CDC-NCM high-speed adapters.
- 📶 **Bluetooth Attacks**: Generic USB Bluetooth dongles supported via `btusb.ko` with RFCOMM TTY (`rfcomm.ko`), BNEP (`bnep.ko`), and HIDP (`hidp.ko`).
- 📁 **Network File Systems**: In-tree NFS client & server (`CONFIG_NFS_FS=y`, `CONFIG_NFSD=y`) and CIFS/SMB (`CONFIG_CIFS=y`) for high-speed network shares.

---

## 🔍 Instant Kernel & Driver Verification (`checker.sh`)

You can instantly audit and verify all NetHunter features, compiled `.ko` drivers, firmware blobs, and `/dev` permissions directly on your rooted Android phone:

```bash
curl -sSL https://cdn.jsdelivr.net/gh/abidhasansojib/gki_kernel_builder@main/checker.sh | su
```

This automated auditor tests:
- ✅ **Kernel Configs**: Audits `/proc/config.gz` for all 80+ NetHunter configs.
- ✅ **Live Drivers & Modules**: Verifies loaded `.ko` modules via `lsmod`.
- ✅ **Firmware Blobs**: Checks firmware presence in `/vendor/firmware` and `/system/etc/firmware`.
- ✅ **Device Nodes & Permissions**: Tests read/write access to `/dev/hidg*`, `/dev/uhid`, `/dev/rfkill`, `/dev/net/tun`, and `/dev/bus/usb/`.

---

## 📱 Tested Devices & Compatibility

> [!TIP]
> **Universal GKI Compatibility**: Because this is a Generic Kernel Image (GKI), you can flash it on **any Android device running on kernel `6.12.30-android16`** (sublevel 30 / 2025-07 patch level).

| Device | Codename | Tested OS Version | Stock Kernel Version | Flashing Mode | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Redmi Note 14 4G** | `tanzanite` | **Xiaomi HyperOS 3.0.302** (Android 16) | `6.12.30-android16-5-g6e872b4863d6-ab13847919-4k` | **Bypass Image** (`do.flash_bypass=1`) | ✅ Fully Working |

> [!CAUTION]
> **CRITICAL COMPATIBILITY & FLASHING WARNINGS**:
> 1. **HyperOS 3.0+ Only**: Do **NOT** flash this kernel on **HyperOS < 3.0** (e.g. HyperOS 1.0 or 2.0 based on Android 14/15). Flashing an Android 16 GKI kernel on older OS versions will cause a **HARD BRICK**.
> 2. **Must Use Bypass-Image on HyperOS**: You **MUST** set `do.flash_bypass=1` in `anykernel.sh` inside the `AnyKernel3.zip` to flash `Bypass-Image`. Flashing the regular `Image` on HyperOS 3 will cause a **bootloop / soft brick** due to strict vendor module version CRC enforcement.

---

## 📋 Installation Instructions

1. **Prerequisites**:
   - Unlocked bootloader.
   - Backup of your current boot image (`boot.img`).
   - Android 16 / HyperOS 3.0+ installed.
   - Flashing utility (e.g. [Kernel Flasher](https://github.com/fatalcoder524/KernelFlasher)).

2. **Flashing Kernel (Bypass Mode)**:
   - Download the generated `AnyKernel3.zip` artifact from the GitHub Actions run or GitHub Release.
   - Extract `anykernel.sh` and ensure `do.flash_bypass=1` is set (or use the built-in bypass installer).
   - Flash the ZIP using Kernel Flasher or custom recovery.
   - Install the matching Manager app for your selected root implementation (KernelSU-Next, KernelSU, or ReSukiSU).
   - Reboot device.

3. **External USB WiFi & NetHunter Tools (Optional)**:
   - Download the `Nethunter-Wireless-Module.zip` module from the release.
   - Flash it in your KernelSU or Magisk manager to load external USB WiFi drivers and firmware blobs automatically on boot.

---

## 🏆 Credits

- 🏗️ **GKI KernelSU SUSFS**: Based on work by [WildKernels](https://github.com/WildKernels/GKI_KernelSU_SUSFS)
- 🔐 **KernelSU**: Developed by [tiann](https://github.com/tiann/KernelSU)
- 🚀 **KernelSU-Next**: Developed by [rifsxd](https://github.com/KernelSU-Next/KernelSU-Next) and [pershoot](https://github.com/pershoot/KernelSU-Next)
- 🛡️ **SUSFS**: Developed by [simonpunk](https://gitlab.com/simonpunk/susfs4ksu.git)
- 🐉 **Kali NetHunter**: Developed by the [Offensive Security / Kali NetHunter Team](https://www.kali.org/docs/nethunter/)
- 🪝 **NoMount**: Developed by [maxsteeel](https://github.com/maxsteeel/nomount)
- 🛡️ **Baseband-guard**: Developed by [vc-teahouse](https://github.com/vc-teahouse/Baseband-guard)
- 📦 **DroidSpaces-OSS**: Developed by [ravindu644](https://github.com/ravindu644/Droidspaces-OSS)
- ⚡ **Kernel Flasher**: Developed by [fatalcoder524](https://github.com/fatalcoder524/KernelFlasher)
