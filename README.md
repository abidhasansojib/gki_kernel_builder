<div align="center">

# GKI Kernel Builder

[![Android](https://img.shields.io/badge/Android-16-blue)](https://android.googlesource.com/)
[![Linux](https://img.shields.io/badge/Kernel-6.12.30-red)](https://kernel.org/)

A feature-packed GKI kernel for Android 16 (`6.12.30-android16`, 2025-07).

</div>

---

## ⚠️ Disclaimer

Flashing custom kernels carries risks. I am not responsible for bricked devices or data loss. Proceed at your own risk.

---

## ✨ Features

- 🔐 **Multi-Root Support**: **KernelSU-Next**, **SukiSU-Ultra**, and **ReSukiSU** with automated manager APK bundling.
- 🛡️ **SUSFS & NoMount**: Built-in SUSFS root hiding and NoMount stealth VFS support.
- 🐉 **Kali NetHunter**: Monitor mode, frame injection, BadUSB HID keyboard/mouse (`/dev/hidg*`), USB Wi-Fi dongles, SDR, CAN bus, and Bluetooth RFCOMM.
- 📱 **Kernel Manager WebUI**: Built-in dashboard to control TCP congestion (BBR3), BadUSB, driver modules, RAM/MGLRU, and root terminal.
- 📦 **NetHunter Wireless Module**: Flashable `Nethunter-Wireless-Modules.zip` with Wi-Fi/SDR drivers, firmware, and WebUI (fully compatible alongside NoMount).
- 🛡️ **Baseband Guard (BBG)**: Partition protection against unauthorized writes.
- 📦 **DroidSpaces-OSS**: Lightweight container runtime support.
- 🚀 **Performance & Networking**: BBRv3, CAKE Qdisc, WireGuard, IP Set, CIFS, NTSync, and scheduler/memory optimizations.
- 🔍 **eBPF & BTF**: In-kernel eBPF kprobes, CO-RE BTF, and FUSE-BPF support.
- ⚡ **Vendor Module Bypass**: Built-in vendor version check bypass ensuring OEM display, touchscreen, and modem drivers load cleanly.

---

## 🐉 Supported NetHunter Hardware & WiFi Adapters

<details>
<summary><b>📡 Supported Wireless WiFi Adapters (Click to Expand)</b></summary>
<br>

| Vendor | Driver | Popular Tested Adapters | Capabilities |
| :--- | :--- | :--- | :--- |
| **MediaTek** | `mt76x2u` / `mt76x0u` | **Alfa AWUS036ACM**, **AWUS036ACHM**, Archer T2U Plus, Netgear A6210 | Dual-band 2.4/5GHz 802.11ac, Monitor Mode, Injection, AP |
| **MediaTek** | `mt7601u` | Generic MT7601U Mini Dongles | 2.4GHz 802.11n, Monitor Mode, Injection |
| **Atheros** | `ath9k_htc` | **TP-Link TL-WN722N v1**, **Alfa AWUS036NHA**, AR9271 | 2.4GHz 802.11n, High-power Injection, AP |
| **Atheros** | `carl9170` | AR9170 based USB dongles | 2.4/5GHz 802.11a/b/g/n, Monitor Mode, Injection |
| **Ralink** | `rt2800usb` | **Alfa AWUS036NH**, **AWUS036NEH**, RT3070, RT2870, RT5370 | 2.4GHz 802.11n, Long-range Injection, AP |
| **Realtek** | `rtw88` | **Alfa AWUS036ACH**, **AWUS036AC**, RTL8812BU, RTL8822BU/CU, RTL8821CU | Dual-band AC1200 / AC1300, Monitor Mode, Injection |
| **Realtek** | `rtl8xxxu` | RTL8188EUS, RTL8192EU, RTL8723AU | 2.4GHz 802.11n, Monitor Mode |
| **Realtek** | `rtl8187` | **Alfa AWUS036H** (RTL8187L) | Legacy 2.4GHz High-power Injection |

</details>

<details>
<summary><b>🛠️ Hardware Gadgets, Network Dongles & SDR (Click to Expand)</b></summary>
<br>

- 🦆 **BadUSB / Rubber Ducky**: Native USB HID keyboard and mouse emulation (`/dev/hidg0`) for NetHunter DuckHunter payloads.
- 📻 **Software Defined Radio (SDR)**: RTL-SDR (`dvb_usb_rtl28xxu`), HackRF One, AirSpy, and Mirics.
- 🚗 **Automotive Hacking (CARsenal)**: SocketCAN framework (`can`, `vcan`, `slcan`, PEAK PCAN-USB, Kvaser, EMS USB).
- 🔌 **USB Serial**: CDC-ACM, FTDI, CH341, CP210X, and PL2303 for router consoles and hardware debugging.
- 🌐 **USB Ethernet**: Realtek RTL8152/RTL8153, ASIX AX88179, CDC-ECM, and CDC-NCM.
- 📶 **Bluetooth**: USB Bluetooth dongles via `btusb` with RFCOMM TTY, BNEP, and HIDP.
- 📁 **Network File Systems**: NFS client & server and CIFS/SMB.

</details>

---

## 📱 NetHunter WebUI Dashboard

Included in `Nethunter-Wireless-Modules.zip`. Open it via the **WebUI** button in your root manager (KernelSU / SukiSU):

- **TCP Control**: Switch congestion algorithms (BBR3, CUBIC, etc.) with one tap.
- **USB / BadUSB**: Switch modes (Stock Android, HID Keyboard/Mouse, Mass Storage, RNDIS).
- **Drivers & Modules**: View and load external Wi-Fi, SDR, and serial drivers on demand.
- **Memory & MGLRU**: View real-time RAM usage, toggle MGLRU, and drop caches.
- **Root Terminal**: Run quick diagnostics (`dmesg`, `lsmod`, `uname -a`).
- **Reset**: Restore default settings anytime with one tap.

---

## 📱 Tested Device & Compatibility

- **Device**: **Redmi Note 14 4G (`tanzanite`)** — fully working.
- **OS / ROM**: Xiaomi HyperOS 3 (Android 16).
- **Target Kernel**: Android 16 GKI (`6.12.30-android16`).
- **Stability**: Tested and verified with **SUSFS + NoMount + NetHunter** running together with full cellular and internal Wi-Fi functionality.

---

## 📋 Installation Instructions

1. **Prerequisites**:
   - Unlocked bootloader.
   - Backup of your current boot image (`boot.img`).
   - **[Kernel Flasher](https://github.com/fatalcoder524/KernelFlasher/releases)** app.

2. **Flash Kernel & Root**:
   - Download the release bundle (`*-Bundle.zip`) and extract it.
   - Flash `*-AnyKernel3.zip` via **Kernel Flasher** or custom recovery.
   - Install the matching root manager APK (`KernelSU_Next_*.apk`, `SukiSU_*.apk`, or `ReSukiSU_*.apk`).
   - Reboot device.
   - *(Optional)* Flash **[susfs4ksu-module](https://github.com/sidex15/susfs4ksu-module/releases)** in your root manager for root hiding.

3. **Modules (Optional)**:
   - **NetHunter**: Flash `Nethunter-Wireless-Modules.zip` in your root manager for USB Wi-Fi/SDR drivers and the WebUI manager.
   - **NoMount**: Flash `NoMount-6.12.30-android16-*.zip` in your root manager for stealth VFS root hiding.
   - *Note: Both modules can be flashed and used together without conflicts.*

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
