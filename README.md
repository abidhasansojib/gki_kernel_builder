<div align="center">

# ⚡ GKI Kernel Builder

[![KernelSU-Next](https://img.shields.io/badge/KernelSU--Next-Supported-green)](https://github.com/KernelSU-Next/KernelSU-Next)
[![SUSFS](https://img.shields.io/badge/SUSFS-v2.2.0-orange)](https://gitlab.com/simonpunk/susfs4ksu)
[![NetHunter](https://img.shields.io/badge/Kali--NetHunter-Ready-blueviolet)](https://www.kali.org/docs/nethunter/)
[![Android](https://img.shields.io/badge/Android-16%20(6.12)-blue)](https://android.googlesource.com/)
[![Linux](https://img.shields.io/badge/Kernel-6.12.30-red)](https://kernel.org/)

**Automated Android 16 (Linux 6.12.30 / 2025-07) Generic Kernel Image (GKI) builder** featuring **KernelSU-Next / KernelSU / ReSukiSU**, **SUSFS v2.2.0**, **NoMount**, and a complete **Kali NetHunter Wireless & Hardware Arsenal**.

</div>

---

## 🔍 Instant Phone Verification (`checker.sh`)

Audit and verify all active NetHunter features, compiled `.ko` drivers, firmware blobs, and `/dev` permissions directly on your rooted device:

```bash
curl -sSL https://cdn.jsdelivr.net/gh/abidhasansojib/gki_kernel_builder@main/checker.sh | su
```

---

## ✨ Features

### 🛡️ Root & Stealth Integration
* **Multi-Root Support**: Choose between **KernelSU-Next**, **KernelSU** (official), and **ReSukiSU**.
* **SUSFS v2.2.0**: Kernel-level root hiding, spoofing (`uname`, `kstat`, `cmdline`), and symbol isolation.
* **NoMount VFS Hooks**: Advanced stealth filesystem hooks with automated collision protection.

### 🐉 Kali NetHunter & Penetration Testing
* **WiFi Injection & Monitor Mode**: Native in-tree `mac80211` and `cfg80211` frame injection.
* **BadUSB / HID Gadgets**: USB HID Keyboard and Mouse emulation (`/dev/hidg0`) for DuckyScript keystroke injection.
* **Flashable Driver Module**: Automatically packages 300+ compiled `.ko` drivers and firmware binaries into `Nethunter-Wireless-Module.zip`.
* **SDR (Software-Defined Radio)**: In-kernel and USB drivers for RTL2832U, HackRF One, AirSpy, and Mirics.
* **Automotive CAN-Bus (CARsenal)**: SocketCAN framework (`can`, `can-raw`, `can-bcm`, `can-gw`), `vcan`, `slcan`, `peak_usb`, and `kvaser_usb`.
* **Hardware Debugging & UART**: `ch341`, `ftdi_sio`, `cp210x`, `pl2303`, and `cdc-acm` for router consoles and RFID tools (Proxmark3).

### 🚀 Performance & Security
* **Baseband Guard (BBG)**: LSM security module protecting critical radio and modem partitions.
* **DroidSpaces-OSS**: Lightweight container runtime support with SYSVIPC kABI fixes.
* **Advanced Networking**: BBRv3, CAKE Qdisc, WireGuard VPN, IP Set, TTL mangling, and in-tree NFS/CIFS.
* **NTSync & BTF**: Low-latency NT synchronization primitives and full eBPF/BTF generation.

---

## 📡 Supported Hardware & Adapters

<details>
<summary><b>📡 Supported Wireless WiFi Adapters (Click to Expand)</b></summary>
<br>

| Vendor | Driver | Popular Tested Adapters | Capabilities |
| :--- | :--- | :--- | :--- |
| **MediaTek** | `mt76x2u` / `mt76x0u` | **Alfa AWUS036ACM**, **Alfa AWUS036ACHM**, Archer T2U Plus | Dual-band 2.4/5GHz 802.11ac, Monitor Mode, Packet Injection, AP Mode |
| **MediaTek** | `mt7601u` | Generic MT7601U Mini Dongles | 2.4GHz 802.11n, Monitor Mode, Packet Injection |
| **Atheros** | `ath9k_htc` | **TP-Link TL-WN722N v1**, **Alfa AWUS036NHA**, AR9271 | 2.4GHz 802.11n, High-power Packet Injection, AP Mode |
| **Atheros** | `carl9170` | AR9170 based USB dongles | 2.4/5GHz 802.11a/b/g/n, Monitor Mode, Packet Injection |
| **Ralink** | `rt2800usb` | **Alfa AWUS036NH**, **Alfa AWUS036NEH**, RT3070, RT5370 | 2.4GHz 802.11n, Long-range Packet Injection, AP Mode |
| **Realtek** | `rtw88_8822bu/cu` | **Alfa AWUS036ACH**, **Alfa AWUS036AC**, RTL8812BU, RTL8822BU | Dual-band AC1200 / AC1300, Monitor Mode, Frame Injection |
| **Realtek** | `rtw88_8821cu/8723du` | RTL8811CU, RTL8821CU, RTL8723DU | AC600 Dual-band Mini Dongles |
| **Realtek** | `rtl8xxxu` / `rtl8187` | RTL8188EUS, RTL8192EU, **Alfa AWUS036H** | 2.4GHz 802.11n / Legacy High-power Injection |

</details>

<details>
<summary><b>🛠️ Hardware Gadgets, Network Dongles & SDR (Click to Expand)</b></summary>
<br>

* 🦆 **BadUSB / Rubber Ducky**: Native USB HID keyboard and mouse emulation (`/dev/hidg0`) for NetHunter DuckHunter payloads.
* 📻 **Software Defined Radio (SDR)**: Drivers for RTL2832U / RTL-SDR (`dvb_usb_rtl28xxu`), HackRF One (`hackrf.ko`), AirSpy (`airspy.ko`), and Mirics (`msi2500.ko` / `msi001.ko`).
* 🚗 **Automotive Hacking (CARsenal)**: SocketCAN framework (`can.ko`, `can-raw.ko`, `can-bcm.ko`, `can-gw.ko`), Virtual CAN (`vcan.ko`), Serial CAN (`slcan.ko`), PEAK PCAN-USB (`peak_usb.ko`), Kvaser (`kvaser_usb.ko`), and EMS USB (`ems_usb.ko`).
* 🔌 **USB Serial & Hardware Hacking**: CDC-ACM (`cdc-acm.ko`), FTDI (`ftdi_sio.ko`), WCH (`ch341.ko`), Silicon Labs (`cp210x.ko`), and Prolific (`pl2303.ko`) for hardware debugging and RFID cloner tools (Proxmark3 / ChameleonMini).
* 🌐 **USB Ethernet Adapters**: Realtek RTL8152 / RTL8153 (`r8152.ko`), ASIX AX88179 / AX8817x (`ax88179_178a.ko`), CDC-ECM, and CDC-NCM high-speed adapters.
* 📶 **Bluetooth Attacks**: USB Bluetooth dongles supported via `btusb.ko` with RFCOMM TTY (`rfcomm.ko`), BNEP (`bnep.ko`), and HIDP (`hidp.ko`).
* 📁 **Network File Systems**: In-tree NFS client & server (`CONFIG_NFS_FS=y`, `CONFIG_NFSD=y`) and CIFS/SMB (`CONFIG_CIFS=y`).

</details>

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
   * Unlocked bootloader.
   * Backup of your current boot image (`boot.img`).
   * Stock kernel based on `6.12.30-android16`.
   * Flashing utility (e.g. [Kernel Flasher](https://github.com/fatalcoder524/KernelFlasher)).

2. **Flashing Kernel (Bypass Mode)**:
   * Download the generated `AnyKernel3.zip` artifact from Releases or Actions.
   * Flash the ZIP using Kernel Flasher or custom recovery.
   * Press **Volume Up (`[VOL+]`)** during flashing to select **Bypass Image**.
   * Install the matching Manager app for your selected root flavor:
     * [KernelSU-Next Manager](https://github.com/KernelSU-Next/KernelSU-Next/releases) *(for KernelSU-Next)*
     * [KernelSU Manager](https://github.com/tiann/KernelSU/releases) *(for official KernelSU)*
     * [ReSukiSU Manager](https://github.com/ReSukiSU/ReSukiSU/releases) *(for ReSukiSU)*
   * Reboot device.

3. **External USB WiFi & NetHunter Drivers (Optional)**:
   * Download `Nethunter-Wireless-Module.zip` from Releases or Actions.
   * Flash it in your **KernelSU-Next, KernelSU, or ReSukiSU** manager to load external USB WiFi drivers and firmware blobs automatically on boot.

---

## 🏆 Credits

* 🏗️ **GKI KernelSU SUSFS**: Based on work by [WildKernels](https://github.com/WildKernels/GKI_KernelSU_SUSFS)
* 🔐 **KernelSU**: Developed by [tiann](https://github.com/tiann/KernelSU)
* 🚀 **KernelSU-Next**: Developed by [rifsxd](https://github.com/KernelSU-Next/KernelSU-Next) and [pershoot](https://github.com/pershoot/KernelSU-Next)
* 🛡️ **SUSFS**: Developed by [simonpunk](https://gitlab.com/simonpunk/susfs4ksu.git)
* 🐉 **Kali NetHunter**: Developed by the [Offensive Security / Kali NetHunter Team](https://www.kali.org/docs/nethunter/)
* 🪝 **NoMount**: Developed by [maxsteeel](https://github.com/maxsteeel/nomount)
* 🛡️ **Baseband-guard**: Developed by [vc-teahouse](https://github.com/vc-teahouse/Baseband-guard)
* 📦 **DroidSpaces-OSS**: Developed by [ravindu644](https://github.com/ravindu644/Droidspaces-OSS)
* ⚡ **Kernel Flasher**: Developed by [fatalcoder524](https://github.com/fatalcoder524/KernelFlasher)
