<div align="center">

# GKI Kernel Builder

[![KernelSU](https://img.shields.io/badge/KernelSU--Next-Supported-green)](https://github.com/pershoot/KernelSU-Next)
[![SUSFS](https://img.shields.io/badge/SUSFS-Integrated-orange)](https://gitlab.com/simonpunk/susfs4ksu)
[![NetHunter](https://img.shields.io/badge/Kali--NetHunter-Ready-blueviolet)](https://www.kali.org/docs/nethunter/)
[![Android](https://img.shields.io/badge/Android-16-blue)](https://android.googlesource.com/)
[![Linux](https://img.shields.io/badge/Kernel-6.12.30-red)](https://kernel.org/)<br>
A GKI kernel builder for kernel 6.12.30-android16, 2025-07.

</div>

---

## ⚠️ Disclaimer

I am **not responsible** for bricked devices, damaged hardware, or any issues that arise from using this kernel.
Please do thorough research and understand the features included before flashing!

---

## ✨ Features

- 🔐 **Multi-Root Support**: Choose between **KernelSU-Next**, **SukiSU-Ultra**, and **ReSukiSU** with automated SUSFS patch integration and automatic Root Manager APK fetching.
- 🛡️ **SUSFS**: Advanced root-hiding kernel patches and userspace integration.
- 🪝 **NoMount VFS Hooks**: Advanced VFS mounting hiding and stealth capabilities with automated hook collision avoidance.
- 🐉 **Kali NetHunter Support**:
  - **Packet Injection & Monitor Mode**: In-tree `mac80211` and `cfg80211` frame injection support.
  - **BadUSB / HID Gadgets**: USB HID Keyboard and Mouse emulation (`/dev/hidg0`) for Rubber Ducky payloads.
  - **USB WiFi Dongle Support**: Realtek (`rtw88` 802.11ac, `rtl8xxxu`, `rtl8187`), Atheros (`ath9k_htc`, `carl9170`), MediaTek (`mt7601u`, `mt76x0u`, `mt76x2u`), and Ralink (`rt2800usb`).
  - **USB Ethernet Adapters**: CDC-ECM, CDC-NCM, Realtek RTL8152, and ASIX AX88179.
  - **Bluetooth RFCOMM & SDR**: Native RFCOMM TTY and RTL-SDR (`rtl28xxu`) support.
- 📦 **Flashable NetHunter Wireless Module**: Automatically packages compiled `.ko` driver modules and official Linux firmware into a flashable KernelSU-Next / SukiSU-Ultra / ReSukiSU module (`Nethunter-Wireless-Modules.zip`) for plug-and-play OTG WiFi support.
- 🛡️ **Baseband Guard (BBG)**: LSM security module for critical partition write protection.
- 📦 **DroidSpaces-OSS**: Lightweight container runtime support with SYSVIPC kABI fixes.
- 🚀 **Networking & Performance**: BBRv3, CAKE Qdisc, WireGuard, IP Set, TTL targets, CIFS, and in-tree memory/caching/IO performance optimization patches.
- ⚡ **NTSync**: Low-latency NT synchronization primitives.
- 🔍 **BTF / eBPF / FUSE-BPF**: Full in-kernel eBPF kprobe/tracepoint events, CO-RE BTF generation, and FUSE-BPF support.

---

## 🐉 Supported NetHunter Hardware & WiFi Adapters

The kernel and accompanying flashable `Nethunter-Wireless-Modules.zip` module provide plug-and-play driver and firmware support for packet injection, monitor mode, AP mode, BadUSB, RTL-SDR, and Bluetooth attacks:

<details>
<summary><b>📡 Supported Wireless WiFi Adapters (Click to Expand)</b></summary>
<br>

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

</details>

<details>
<summary><b>🛠️ Hardware Gadgets, Network Dongles & SDR (Click to Expand)</b></summary>
<br>

- 🦆 **BadUSB / Rubber Ducky**: Native USB HID keyboard and mouse emulation (`/dev/hidg0`) for NetHunter DuckHunter payloads.
- 📻 **Software Defined Radio (SDR)**: In-kernel and USB drivers for RTL2832U / RTL-SDR (`dvb_usb_rtl28xxu`), HackRF One (`hackrf.ko`), AirSpy (`airspy.ko`), and Mirics (`msi2500.ko` / `msi001.ko`).
- 🚗 **Automotive Hacking (CARsenal)**: SocketCAN framework (`can.ko`, `can-raw.ko`, `can-bcm.ko`, `can-gw.ko`), Virtual CAN (`vcan.ko`), Serial CAN (`slcan.ko`), PEAK PCAN-USB (`peak_usb.ko`), Kvaser (`kvaser_usb.ko`), and EMS USB (`ems_usb.ko`).
- 🔌 **USB Serial & Hardware Hacking**: CDC-ACM (`cdc-acm.ko`), FTDI (`ftdi_sio.ko`), WCH (`ch341.ko`), Silicon Labs (`cp210x.ko`), and Prolific (`pl2303.ko`) for router consoles, embedded hardware debugging, and RFID cloner tools (Proxmark3 / ChameleonMini).
- 🌐 **USB Ethernet Adapters**: Realtek RTL8152 / RTL8153 (`r8152.ko`), ASIX AX88179 / AX8817x (`ax88179_178a.ko`), CDC-ECM, and CDC-NCM high-speed adapters.
- 📶 **Bluetooth Attacks**: Generic USB Bluetooth dongles supported via `btusb.ko` with RFCOMM TTY (`rfcomm.ko`), BNEP (`bnep.ko`), and HIDP (`hidp.ko`).
- 📁 **Network File Systems**: In-tree NFS client & server (`CONFIG_NFS_FS=y`, `CONFIG_NFSD=y`) and CIFS/SMB (`CONFIG_CIFS=y`) for high-speed network shares.

</details>

---

## 📱 Tested Device & Compatibility

* **Tested Device**: **Redmi Note 14 4G (`tanzanite`)** &mdash; everything is fully working!
* **Target Kernel**: **Android 16 (`6.12.30-android16`)** GKI only.
* **Compatibility**: Optimized for Xiaomi HyperOS 3 (Android 16). The kernel automatically integrates the vendor module version-check bypass hack, ensuring OEM hardware drivers (touchscreen, display, modem, sensors) load seamlessly without bootloops.

---

## 📋 Installation Instructions

1. **Prerequisites**:
   - Unlocked bootloader.
   - Backup of your current boot image (`boot.img`).
   - Stock kernel based on `6.12.30-android16`.
   - Flashing utility (e.g. [Kernel Flasher](https://github.com/fatalcoder524/KernelFlasher) or custom recovery).

2. **Flashing Kernel**:
   - Download the generated `AnyKernel3.zip` artifact from Releases or Actions.
   - Flash the ZIP using Kernel Flasher or custom recovery (vendor module version bypass is applied automatically).
   - Install the matching Manager app for your selected root flavor:
     - [KernelSU-Next Manager](https://github.com/KernelSU-Next/KernelSU-Next/releases) *(for KernelSU-Next)*
     - [SukiSU-Ultra Manager](https://github.com/SukiSU-Ultra/SukiSU-Ultra/releases) *(for SukiSU-Ultra)*
     - [ReSukiSU Manager](https://github.com/ReSukiSU/ReSukiSU/releases) *(for ReSukiSU)*
   - Reboot device.

3. **External USB WiFi & NetHunter Tools (Optional)**:
   - Download the `Nethunter-Wireless-Modules.zip` module from the release.
   - Flash it in your KernelSU-Next, SukiSU-Ultra, or ReSukiSU manager to load external USB WiFi drivers and firmware blobs automatically on boot.

---

## 🏆 Credits

- 🏗️ **GKI KernelSU SUSFS**: Based on work by [WildKernels](https://github.com/WildKernels/GKI_KernelSU_SUSFS)
- 🚀 **KernelSU-Next**: Developed by [rifsxd](https://github.com/KernelSU-Next/KernelSU-Next) and [pershoot](https://github.com/pershoot/KernelSU-Next)
- 🔐 **SukiSU-Ultra**: Developed by [SukiSU-Ultra](https://github.com/SukiSU-Ultra/SukiSU-Ultra)
- 💫 **ReSukiSU**: Developed by [ReSukiSU](https://github.com/ReSukiSU/ReSukiSU)
- 🛡️ **SUSFS**: Developed by [simonpunk](https://gitlab.com/simonpunk/susfs4ksu.git)
- 🐉 **Kali NetHunter**: Developed by the [Offensive Security / Kali NetHunter Team](https://www.kali.org/docs/nethunter/)
- 🪝 **NoMount**: Developed by [maxsteeel](https://github.com/maxsteeel/nomount)
- 🛡️ **Baseband-guard**: Developed by [vc-teahouse](https://github.com/vc-teahouse/Baseband-guard)
- 📦 **DroidSpaces-OSS**: Developed by [ravindu644](https://github.com/ravindu644/Droidspaces-OSS)
- ⚡ **Kernel Flasher**: Developed by [fatalcoder524](https://github.com/fatalcoder524/KernelFlasher)
