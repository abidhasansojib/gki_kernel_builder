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
- 📦 **Flashable NetHunter Wireless Module**: Automatically packages compiled `.ko` driver modules and official Linux firmware into a flashable KernelSU/Magisk module (`NetHunter-Wireless.zip`) for plug-and-play OTG WiFi support.
- 🛡️ **Baseband Guard (BBG)**: LSM security module for critical partition write protection.
- 📦 **DroidSpaces-OSS**: Lightweight container runtime support with SYSVIPC kABI fixes.
- 🚀 **Networking & Performance**: BBRv3, CAKE Qdisc, WireGuard, IP Set, TTL targets, CIFS.
- ⚡ **NTSync**: Low-latency NT synchronization primitives.
- 🔍 **BTF / eBPF**: BTF generation, eBPF tooling, and FUSE-BPF support.

---

## 📋 Installation Instructions

1. **Prerequisites**:
   - Unlocked bootloader.
   - Backup of your current boot image.
   - Flashing utility (e.g. [Kernel Flasher](https://github.com/fatalcoder524/KernelFlasher)).

2. **Flashing Kernel**:
   - Download the generated `AnyKernel3.zip` artifact from the GitHub Actions run or GitHub Release.
   - Flash the ZIP using Kernel Flasher or custom recovery.
   - Install the matching Manager app for your selected root implementation (KernelSU-Next, KernelSU, or ReSukiSU).
   - Reboot device.

3. **External USB WiFi & NetHunter Tools (Optional)**:
   - Download the `NetHunter-Wireless.zip` module from the release.
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
