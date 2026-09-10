<div align="center">

# GKI Kernel Builder

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
  - **BadUSB / HID Gadgets**: USB HID Keyboard and Mouse emulation (`/dev/hidg0`, `/dev/hidg1`) for Rubber Ducky payloads and OTG attacks.
  - **USB WiFi Dongle Support**: Realtek (`rtw88` 802.11ac, `rtl8xxxu`, `rtl8187`), Atheros (`ath9k_htc`, `carl9170`), MediaTek (`mt7601u`, `mt76x0u`, `mt76x2u`), and Ralink (`rt2800usb`).
  - **USB Ethernet Adapters**: CDC-ECM, CDC-NCM, Realtek RTL8152, and ASIX AX88179.
  - **Bluetooth RFCOMM & SDR**: Native RFCOMM TTY and RTL-SDR (`rtl28xxu`) support.
- 📱 **Material 3 Kernel Manager WebUI**: Standalone mobile-optimized dashboard built into `Nethunter-Wireless-Modules.zip` with live hardware telemetry, dynamic TCP congestion switching (BBR3/BBR/Cubic), BadUSB mode switching, dynamic module loading, MGLRU/RAM control, and rooted web terminal console.
- 📦 **Flashable NetHunter Wireless Module**: Automatically packages compiled `.ko` driver modules, official Linux firmware, zero-drain native ueventd rules, WebUI, and Action launcher into a single flashable module (`Nethunter-Wireless-Modules.zip`).
- 🛡️ **Baseband Guard (BBG)**: LSM security module for critical partition write protection.
- 📦 **DroidSpaces-OSS**: Lightweight container runtime support with SYSVIPC kABI fixes.
- 🚀 **Networking & Performance**: BBRv3, CAKE Qdisc, WireGuard, IP Set, TTL targets, CIFS, and in-tree memory/caching/IO performance optimization patches (`schedutil` CPU governor default).
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

## 📱 NetHunter Kernel Manager WebUI Dashboard

The flashable `Nethunter-Wireless-Modules.zip` module integrates an interactive **Material 3 Kernel Manager WebUI** (`webroot/index.html`) accessible directly within your root manager or mobile browser:

* 🌐 **Direct Root Bridge Execution**: Native interface support for **KernelSU**, **APatch**, **SukiSU**, and **ReSukiSU** WebUI bridges (`window.ksu` / `window.suki`). Automatically detects environment and provides a graceful, safe read-only preview mode when opened in standard web browsers.
* 📶 **Dynamic TCP Congestion Switcher**: Live detection of all in-kernel algorithms (`BBR3`, `BBR`, `Cubic`, `WestWood`, etc.) from `/proc/sys/net/ipv4/tcp_available_congestion_control`. Features one-tap switching and automatic boot persistence via `/data/adb/service.d/00-bbr.sh`.
* 🦆 **BadUSB HID & Gadget Switcher**: Toggle effortlessly between Stock Android USB (MTP + ADB), BadUSB HID Keyboard & Mouse (`/dev/hidg0`, `/dev/hidg1`), USB Mass Storage, and RNDIS Ethernet. Includes an on-screen DuckyScript test keystroke injector.
* 🔌 **Dynamic Driver & Firmware Manager**: Filter and view 75+ modular drivers by category (WiFi, Serial, Ethernet, SDR, CAN). Auto-loads kernel modules from `lkm/` with automatic multi-tier dependency resolution and safe reverse-order unbinding.
* 🧠 **Memory & MGLRU Telemetry**: Real-time `/proc/meminfo` calculation ($Used = Total - Available$), ZRAM compression algorithm & disk size telemetry, VFS cache pressure adjustments, swappiness tuning, and one-tap MGLRU `0x0007` locking.
* ⚡ **Optimized CPU Governor Default**: Pre-configured with the responsive `schedutil` governor by default in kernel and boot services, keeping the UI clean while allowing fine-grained user tuning via external tools like FKM.
* 💻 **Rooted Terminal Console**: Built-in dark terminal with command history, preset diagnostic shortcuts (`uname -a`, `lsmod`, `ip link`, `dmesg`), and clipboard export.
* 🔄 **Subsystem Reset Buttons**: Dedicated Reset button on every menu to safely revert network, USB, driver, or memory settings back to kernel defaults.
* 📂 **Universal Storage Sync & Action Launcher**: WebUI is automatically synced to `/storage/emulated/0/Download/nethunter_webui.html` on boot (including TWRP recovery installs) and can be opened immediately via the root manager's **Action** button (`action.sh`).

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
   - Flashing utility: **[Kernel Flasher](https://github.com/fatalcoder524/KernelFlasher/releases)** app.

2. **Flashing Kernel & Root Setup**:
   - Download the generated all-in-one release package (`*-Bundle.zip`) from Releases or Actions and extract it.
   - Flash `*-AnyKernel3.zip` using the **[Kernel Flasher](https://github.com/fatalcoder524/KernelFlasher/releases)** app (vendor module version bypass is applied automatically).
   - Install the matching Manager APK extracted from the bundle (`KernelSU_Next_*.apk`, `SukiSU_*.apk`, or `ReSukiSU_*.apk`).
   - Reboot device.
   - Flash **[susfs4ksu-module (by sidex15)](https://github.com/sidex15/susfs4ksu-module/releases)** in your Root Manager to activate kernel-level root hiding.

3. **External USB WiFi & NetHunter WebUI Manager (Optional)**:
   - Download the `Nethunter-Wireless-Modules.zip` module from the release.
   - Flash it in your KernelSU-Next, SukiSU-Ultra, ReSukiSU, or APatch manager.
   - Tap **WebUI** under the module in your root manager to launch the interactive Kernel Manager dashboard with live root execution!
   - Alternatively, tap **Action** or open `/storage/emulated/0/Download/nethunter_webui.html` in your browser.

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
