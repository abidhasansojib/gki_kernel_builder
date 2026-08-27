# GKI Kernel Builder (Android 16 / 6.12 GKI)

[![KernelSU-Next](https://img.shields.io/badge/KernelSU--Next-Supported-green)](https://github.com/KernelSU-Next/KernelSU-Next)
[![SUSFS](https://img.shields.io/badge/SUSFS-v2.2.0-orange)](https://gitlab.com/simonpunk/susfs4ksu)
[![NetHunter](https://img.shields.io/badge/Kali--NetHunter-Ready-blueviolet)](https://www.kali.org/docs/nethunter/)
[![Android](https://img.shields.io/badge/Android-16%20(6.12)-blue)](https://android.googlesource.com/)

Automated GitHub Actions builder for **Android 16 (Linux 6.12 GKI)** Generic Kernel Images featuring **KernelSU-Next / KernelSU / ReSukiSU**, **SUSFS v2.2.0**, **NoMount**, and a full **Kali NetHunter Wireless Arsenal**.

---

## 🔍 Instant Phone Verification (`checker.sh`)

Test and verify all NetHunter features, compiled `.ko` drivers, firmware, and device permissions directly on your rooted device:

```bash
curl -sSL https://cdn.jsdelivr.net/gh/abidhasansojib/gki_kernel_builder@main/checker.sh | su
```

---

## ✨ Features

* 🔐 **Root & Stealth**: KernelSU-Next / KernelSU / ReSukiSU with **SUSFS v2.2.0** and **NoMount** VFS stealth.
* 🐉 **Kali NetHunter Arsenal**:
  * **WiFi Injection & Monitor Mode**: In-tree `mac80211` / `cfg80211` frame injection.
  * **BadUSB / HID Gadgets**: USB HID Keyboard and Mouse emulation (`/dev/hidg0`) for keystroke injection.
  * **External USB WiFi**: Realtek (`rtw88`, `rtl8xxxu`, `rtl8187`), Atheros (`ath9k_htc`, `carl9170`), MediaTek (`mt76`), and Ralink (`rt2800usb`).
  * **SDR (Software-Defined Radio)**: Native drivers for HackRF One, AirSpy, Mirics, and RTL-SDR (`rtl28xxu`).
  * **Automotive CAN-Bus (CARsenal)**: SocketCAN (`can`, `can-raw`, `can-bcm`), `vcan`, `slcan`, `peak_usb`, `kvaser_usb`.
  * **USB UART Serial**: `ch341`, `ftdi_sio`, `cp210x`, `pl2303`, `cdc-acm` for hardware debugging and RFID tools.
* 📦 **Flashable NetHunter Module**: Automatically packages all 300+ compiled `.ko` modules and firmware binaries into `Nethunter-Wireless-Module.zip`.
* 🛡️ **Baseband Guard (BBG)**: LSM protection for critical radio partitions.
* 📦 **DroidSpaces-OSS**: Lightweight container runtime support.
* 🚀 **Networking**: BBRv3, CAKE Qdisc, WireGuard, IP Set, TTL hotspot targets, and in-tree NFS/CIFS.

---

## 📡 Tested USB WiFi Adapters

| Vendor | Driver | Popular Tested Models | Capabilities |
| :--- | :--- | :--- | :--- |
| **MediaTek** | `mt76x2u` / `mt76x0u` | **Alfa AWUS036ACM / ACHM**, Archer T2U Plus | Dual-band 2.4/5GHz 802.11ac, Monitor Mode, Injection, AP |
| **MediaTek** | `mt7601u` | Generic MT7601U Mini Dongles | 2.4GHz 802.11n, Monitor Mode, Injection |
| **Atheros** | `ath9k_htc` | **TP-Link TL-WN722N v1**, **Alfa AWUS036NHA**, AR9271 | 2.4GHz 802.11n, High-power Injection, AP Mode |
| **Atheros** | `carl9170` | AR9170 USB Dongles | Dual-band 802.11a/b/g/n, Monitor Mode, Injection |
| **Ralink** | `rt2800usb` | **Alfa AWUS036NH / NEH**, RT3070, RT5370 | 2.4GHz 802.11n, Long-range Injection, AP Mode |
| **Realtek** | `rtw88_8822bu/cu` | **Alfa AWUS036ACH / AC**, RTL8812BU, RTL8822BU | Dual-band AC1200 / AC1300, Monitor Mode, Injection |
| **Realtek** | `rtl8xxxu` / `rtl8187` | RTL8188EUS, RTL8192EU, **Alfa AWUS036H** | 2.4GHz 802.11n / Legacy High-power Injection |

---

## 📱 Compatibility & Flashing

| Device | Codename | OS | Flashing Target | Status |
| :--- | :--- | :--- | :--- | :--- |
| **Universal GKI** | Any GKI 6.12 device | Android 16 (6.12) | Standard `Image` | ✅ Supported |
| **Redmi Note 14 4G** | `tanzanite` | HyperOS 3.0 (Android 16) | **Bypass Image** (`do.flash_bypass=1`) | ✅ Verified |

> [!WARNING]
> **HyperOS 3.0+ Warning**: When flashing on Xiaomi HyperOS, you **must** set `do.flash_bypass=1` in `anykernel.sh` inside `AnyKernel3.zip` to bypass vendor module CRC checks. Do NOT flash on older Android 14/15 ROMs.

---

## 🚀 Installation

1. **Flash Kernel**: Download `AnyKernel3.zip` from Releases/Actions and flash via [Kernel Flasher](https://github.com/fatalcoder524/KernelFlasher). *(Set `do.flash_bypass=1` if on HyperOS).*
2. **Install Root Manager**: Install the [KernelSU-Next Manager APK](https://github.com/KernelSU-Next/KernelSU-Next/releases).
3. **Flash NetHunter Drivers (Optional)**: Flash `Nethunter-Wireless-Module.zip` in KernelSU/Magisk for OTG USB WiFi plug-and-play support.

---

## 🏆 Credits

* [WildKernels](https://github.com/WildKernels/GKI_KernelSU_SUSFS) &bull; [KernelSU-Next](https://github.com/KernelSU-Next/KernelSU-Next) &bull; [tiann](https://github.com/tiann/KernelSU) &bull; [SUSFS (simonpunk)](https://gitlab.com/simonpunk/susfs4ksu.git) &bull; [Kali NetHunter](https://www.kali.org/docs/nethunter/) &bull; [NoMount](https://github.com/maxsteeel/nomount) &bull; [Baseband-guard](https://github.com/vc-teahouse/Baseband-guard) &bull; [DroidSpaces](https://github.com/ravindu644/Droidspaces-OSS) &bull; [Kernel Flasher](https://github.com/fatalcoder524/KernelFlasher)
