<div align="center">

# GKI Kernel Builder

[![KernelSU-Next](https://img.shields.io/badge/KernelSU--Next-Supported-green)](https://github.com/KernelSU-Next/KernelSU-Next)
[![SUSFS](https://img.shields.io/badge/SUSFS-v2.2.0-orange)](https://gitlab.com/simonpunk/susfs4ksu)
[![NetHunter](https://img.shields.io/badge/Kali--NetHunter-Ready-blueviolet)](https://www.kali.org/docs/nethunter/)
[![Android](https://img.shields.io/badge/Android-16%20(6.12)-blue)](https://android.googlesource.com/)
[![Linux](https://img.shields.io/badge/Kernel-6.12.30-red)](https://kernel.org/)<br>
A Generic Kernel Image (GKI) builder for **Android 16 (`6.12.30-android16`, 2025-07)** with **Multi-Root**, **SUSFS v2.2.0**, **NoMount**, and a complete **Kali NetHunter Wireless Stack**.

</div>

---

## ⚠️ Disclaimer

I am **not responsible** for bricked devices, bootloops, or hardware damage. Flash at your own risk.

---

## ✨ Features

- 🔐 **Multi-Root**: KernelSU-Next, official KernelSU, and ReSukiSU with automated SUSFS patch integration.
- 🛡️ **SUSFS v2.2.0**: Kernel-level root hiding, mount spoofing (`mnt_id`), kstat spoofing, and symbol isolation.
- 🪝 **NoMount**: VFS mounting stealth hooks with automated collision protection.
- 🐉 **Kali NetHunter Suite**:
  - **WiFi Monitor Mode & Injection**: In-tree `mac80211` and `cfg80211` packet injection.
  - **BadUSB HID Gadgets**: Keystroke injection via `/dev/hidg0` (keyboard/mouse emulation).
  - **Modular Drivers**: Realtek (`rtw88`, `rtl8xxxu`, `rtl8187`), Atheros (`ath9k_htc`, `carl9170`), MediaTek (`mt76`), Ralink (`rt2800usb`), and ZyDAS (`zd1211rw`).
  - **SDR & Radio**: RTL-SDR (`rtl28xxu`), HackRF One, AirSpy, and Mirics drivers.
  - **Automotive (CAN-Bus)**: SocketCAN (`can`, `can-raw`, `can-bcm`, `can-gw`), `vcan`, `slcan`, `peak_usb`, `kvaser_usb`.
  - **Hardware Serial**: `ch341`, `ftdi_sio`, `cp210x`, `pl2303`, `cdc-acm` for UART debugging and RFID tools.
- 📦 **Flashable NetHunter Module**: Bundles all 300+ compiled `.ko` drivers and firmware binaries into `Nethunter-Wireless-Module.zip`.
- 🛡️ **Baseband Guard (BBG)**: LSM write-protection for critical radio and modem partitions.
- 📦 **DroidSpaces-OSS**: Lightweight container runtime support.
- 🚀 **Networking & Performance**: BBRv3, CAKE Qdisc, WireGuard, IP Set, TTL mangling, and in-tree NFS/CIFS.
- ⚡ **NTSync & BTF**: Low-latency NT synchronization primitives and eBPF/BTF generation.

---

## 🐉 Supported NetHunter Hardware & WiFi Adapters

The kernel and accompanying `Nethunter-Wireless-Module.zip` provide plug-and-play driver and firmware support for packet injection, monitor mode, AP mode, BadUSB, RTL-SDR, and Bluetooth:

<details>
<summary><b>📡 Supported Wireless WiFi Adapters (Click to Expand)</b></summary>
<br>

| Vendor | Driver | Popular Tested Adapters | Capabilities |
| :--- | :--- | :--- | :--- |
| **MediaTek** | `mt76x2u` / `mt76x0u` | **Alfa AWUS036ACM / ACHM**, Archer T2U Plus | Dual-band 2.4/5GHz 802.11ac, Monitor Mode, Injection, AP |
| **MediaTek** | `mt7601u` | Generic MT7601U Mini Dongles | 2.4GHz 802.11n, Monitor Mode, Injection |
| **Atheros** | `ath9k_htc` | **TP-Link TL-WN722N v1**, **Alfa AWUS036NHA**, AR9271 | 2.4GHz 802.11n, High-power Injection, AP Mode |
| **Atheros** | `carl9170` | AR9170 based USB dongles | Dual-band 802.11a/b/g/n, Monitor Mode, Injection |
| **Ralink** | `rt2800usb` | **Alfa AWUS036NH / NEH**, RT3070, RT5370 | 2.4GHz 802.11n, Long-range Injection, AP Mode |
| **Realtek** | `rtw88_8822bu/cu` | **Alfa AWUS036ACH / AC**, RTL8812BU, RTL8822BU | Dual-band AC1200 / AC1300, Monitor Mode, Injection |
| **Realtek** | `rtw88_8821cu/8723du` | RTL8811CU, RTL8821CU, RTL8723DU | AC600 Dual-band Mini Dongles |
| **Realtek** | `rtl8xxxu` / `rtl8187` | RTL8188EUS, RTL8192EU, **Alfa AWUS036H** | 2.4GHz 802.11n, Monitor Mode / High-power Injection |

</details>

<details>
<summary><b>🛠️ Hardware Gadgets, Network Dongles & SDR (Click to Expand)</b></summary>
<br>

- 🦆 **BadUSB / Rubber Ducky**: Native USB HID keyboard and mouse emulation (`/dev/hidg0`) for keystroke injection.
- 📻 **Software Defined Radio (SDR)**: RTL2832U / RTL-SDR (`dvb_usb_rtl28xxu`), HackRF One (`hackrf.ko`), AirSpy (`airspy.ko`), and Mirics (`msi2500.ko` / `msi001.ko`).
- 🚗 **Automotive Hacking (CARsenal)**: SocketCAN framework (`can.ko`, `can-raw.ko`, `can-bcm.ko`, `can-gw.ko`), Virtual CAN (`vcan.ko`), Serial CAN (`slcan.ko`), PEAK PCAN-USB (`peak_usb.ko`), Kvaser (`kvaser_usb.ko`), and EMS USB (`ems_usb.ko`).
- 🔌 **USB Serial & Hardware Hacking**: CDC-ACM (`cdc-acm.ko`), FTDI (`ftdi_sio.ko`), WCH (`ch341.ko`), Silicon Labs (`cp210x.ko`), and Prolific (`pl2303.ko`) for router consoles and RFID tools (Proxmark3 / ChameleonMini).
- 🌐 **USB Ethernet Adapters**: Realtek RTL8152 / RTL8153 (`r8152.ko`), ASIX AX88179 / AX8817x (`ax88179_178a.ko`), CDC-ECM, and CDC-NCM high-speed adapters.
- 📶 **Bluetooth Attacks**: USB Bluetooth dongles supported via `btusb.ko` with RFCOMM TTY (`rfcomm.ko`), BNEP (`bnep.ko`), and HIDP (`hidp.ko`).
- 📁 **Network File Systems**: In-tree NFS client & server (`CONFIG_NFS_FS=y`, `CONFIG_NFSD=y`) and CIFS/SMB (`CONFIG_CIFS=y`).

</details>

---

## 🔍 Instant Kernel & Driver Verification (`checker.sh`)

Audit and verify all NetHunter features, compiled `.ko` drivers, firmware blobs, and `/dev` permissions directly on your rooted Android phone:

```bash
curl -sSL https://cdn.jsdelivr.net/gh/abidhasansojib/gki_kernel_builder@main/checker.sh | su
```

Tests performed:
- ✅ **Kernel Configs**: Audits `/proc/config.gz` for all 80+ NetHunter configs.
- ✅ **Live Drivers & Modules**: Verifies loaded `.ko` modules via `lsmod`.
- ✅ **Firmware Blobs**: Checks firmware presence in `/vendor/firmware` and `/system/etc/firmware`.
- ✅ **Device Nodes & Permissions**: Tests read/write access to `/dev/hidg*`, `/dev/uhid`, `/dev/rfkill`, `/dev/net/tun`, and `/dev/bus/usb/`.

---

## 📱 Tested Device & Compatibility

* **Tested Device**: **Redmi Note 14 4G (`tanzanite`)** &mdash; everything is fully working!
* **Target Kernel**: **Android 16 (`6.12.30-android16`)** GKI only.
* **Xiaomi HyperOS 3.0 Warning**:
  * For **HyperOS 3.0+ only** (Android 16). Do **NOT** flash on HyperOS 1.0 or 2.0 (Android 14/15) or you will brick your device.
  * When flashing `AnyKernel3.zip`, press the **Volume Up (`[VOL+]`)** button to flash **Bypass-Image** and bypass vendor module CRC checks.

---

## 📋 Installation Instructions

1. **Prerequisites**:
   - Unlocked bootloader.
   - Backup of your current boot image (`boot.img`).
   - Stock kernel based on `6.12.30-android16`.
   - Flashing utility (e.g. [Kernel Flasher](https://github.com/fatalcoder524/KernelFlasher)).

2. **Flashing Kernel (Bypass Mode)**:
   - Download `AnyKernel3.zip` from Releases or Actions.
   - Flash the ZIP using Kernel Flasher or custom recovery.
   - Press **Volume Up (`[VOL+]`)** during flashing to select **Bypass Image**.
   - Install the matching Manager app for your selected root flavor:
     - [KernelSU-Next Manager](https://github.com/KernelSU-Next/KernelSU-Next/releases) *(for KernelSU-Next)*
     - [KernelSU Manager](https://github.com/tiann/KernelSU/releases) *(for official KernelSU)*
     - [ReSukiSU Manager](https://github.com/ReSukiSU/ReSukiSU/releases) *(for ReSukiSU)*
   - Reboot device.

3. **External USB WiFi & NetHunter Tools (Optional)**:
   - Download `Nethunter-Wireless-Module.zip` from Releases or Actions.
   - Flash it in your KernelSU-Next, KernelSU, or ReSukiSU manager to load external USB WiFi drivers and firmware blobs automatically on boot.

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
