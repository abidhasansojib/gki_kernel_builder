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

- 🔐 **Root Stack**: **SukiSU-Nova** (formerly SukiSU-Ultra) with native SUSFS v2.4.0 root hiding, KPM support, built-in NyaZygisk, and automated `arm64-v8a` manager APK bundling.
- 🛡️ **SUSFS & NoMount**: Built-in SUSFS v2.4.0 root hiding (`sus_path_uid_filter`, `priority_uid_filter`), NoMount v2.3.1 stealth VFS support, and FUSE-compatible Scoped-Storage Unicode Guard (preserves emojis).
- 🐉 **USB Arsenal & Wireless Driver Stack**: Built-in BadUSB HID keyboard/mouse (`/dev/hidg1`, `/dev/hidg2` with configurable `bInterval` polling), PiKVM DVD-ROM emulation (booting >2.36GB ISOs via USB Arsenal / DriveDroid), monitor mode, frame injection, modern USB Wi-Fi dongles, USB Gigabit Ethernet, USB Serial, and Bluetooth RFCOMM.
- 📱 **Kernel Manager WebUI**: Streamlined Material 3 dashboard to control TCP congestion (BBR default / CUBIC / Westwood+ / BIC / HTCP), driver modules, RAM/MGLRU, and real-time activity log.
- 📦 **Wireless & Hardware Module**: Flashable `Nethunter-Wireless-Modules.zip` with modern Wi-Fi/Ethernet/Serial/Bluetooth `.ko` drivers, firmware, and WebUI (fully compatible alongside NoMount and DroidSpaces).
- 🛡️ **Baseband Guard (BBG)**: Partition protection against unauthorized writes.
- 📦 **DroidSpaces-OSS**: Lightweight container runtime support with SYSVIPC and cgroup v2 CPU/process limits (`CONFIG_CFS_BANDWIDTH=y`, `CONFIG_CGROUP_PIDS=y`).
- 🚀 **Performance & Networking**: Mainline BBR, CUBIC, Westwood+, BIC, HTCP, CAKE Qdisc, WireGuard, IP Set, CIFS, NTSync, and scheduler/memory optimizations.
- 🔍 **eBPF & BTF**: In-kernel eBPF kprobes, CO-RE BTF, and FUSE-BPF support.
- ⚡ **Vendor Module Bypass**: Built-in vendor version check bypass ensuring OEM display, touchscreen, and modem drivers load cleanly.

---

## 🐉 Supported NetHunter Hardware & WiFi Adapters

<details>
<summary><b>📡 Supported Wireless WiFi Adapters (Click to Expand)</b></summary>
<br>

| Vendor | Driver | Popular Tested Adapters | Capabilities |
| :--- | :--- | :--- | :--- |
| **MediaTek** | `mt76x2u` / `mt76x0u` | **Alfa AWUS036ACM** (MT7612U), **Alfa AWUS036ACHM** (MT7610U), Archer T2U Plus v1, Netgear A6210, Panda PAU0B | Dual-band 2.4/5GHz 802.11ac, Monitor Mode, Injection, AP |
| **MediaTek** | `mt7601u` | Generic MT7601U Mini Dongles, TP-Link TL-WN727N v5 | 2.4GHz 802.11n, Monitor Mode, Injection |
| **Atheros** | `ath9k_htc` | **TP-Link TL-WN722N v1** (AR9271), **Alfa AWUS036NHA**, AR9271 / AR7010 Generic Dongles | 2.4GHz 802.11n, High-power Injection, AP |
| **Atheros** | `carl9170` | **TP-Link TL-WN821N v2**, D-Link DWA-160 vA1/vA2, Netgear WNDA3100 v1 (AR9170) | Dual-band 2.4/5GHz 802.11a/b/g/n, Monitor Mode, Injection, AP |
| **Ralink** | `rt2800usb` | **Alfa AWUS036NH**, **Alfa AWUS036NEH**, Panda PAU05/PAU06/PAU09 (RT5572), RT3070, RT5370 | 2.4GHz & 5GHz 802.11n, Long-range Injection, AP |
| **Realtek** | `rtw88` | **Edimax EW-7822ULC** (RTL8822BU), **TP-Link Archer T2U Nano / Plus v2** (RTL8821CU), **Comfast CF-924AC v2** (RTL8822CU), ASUS USB-AC53 Nano | Dual-band 2.4/5GHz 802.11ac, Monitor Mode, Injection |
| **Realtek** | `rtl8xxxu` | **TP-Link TL-WN725N v2/v3** (RTL8188EUS), **TL-WN823N** (RTL8192EU), Edimax EW-7811Un v1/v2, D-Link DWA-131 | 2.4GHz 802.11n, Monitor Mode |

</details>

<details>
<summary><b>🛠️ Hardware Gadgets, USB Ethernet, Serial & Bluetooth (Click to Expand)</b></summary>
<br>

- 🦆 **BadUSB / Rubber Ducky & USB Arsenal (Built-in)**: Native USB HID keyboard and mouse emulation (`/dev/hidg1` for keyboard, `/dev/hidg2` for mouse, with writable ConfigFS `interval` polling rate), multi-gadget ConfigFS support, PiKVM DVD-ROM emulation for booting >2.36GB ISO images, and USB NCM/ECM/RNDIS Ethernet tethering NAT.
- 🌐 **USB Ethernet**: Realtek RTL8152/RTL8153, ASIX AX88179, CDC-ECM, and CDC-NCM (for wired LAN & DroidSpaces `--net=macvlan`).
- 🔌 **USB Serial (UART)**: CDC-ACM, FTDI, CH341, CP210X, and PL2303 for router consoles, ESP32/Arduino, and hardware debugging.
- 📶 **Bluetooth**: External USB Bluetooth dongles via `btusb` with RFCOMM TTY, BNEP, and HIDP.
- 📁 **Network File Systems**: Built-in CIFS/SMB support.

</details>

> [!TIP]
> **💡 Internal Wi-Fi (`wlan0`) & PixieDust / WPS Testing:**  
> On MediaTek and Android SoC devices, turning off Wi-Fi triggers an OEM vendor power-collapse that unregisters `wlan0` (`Could not set interface flags (UP): No such device`).  
> When running PixieDust or WPS testing tools (e.g., Stryker, Oneshot, PixieWps) on the internal `wlan0` interface, **turn on your mobile Hotspot** before launching the test. The active Hotspot holds a kernel wakelock on the Wi-Fi baseband and prevents the driver from powering down, keeping `wlan0` alive without needing an external USB adapter.

---

## 📱 NetHunter WebUI Dashboard

Included in `Nethunter-Wireless-Modules.zip`. Open it via the **WebUI** button in your root manager (KernelSU / SukiSU):

- **Network & TCP Control**: Switch congestion algorithms (BBR default, CUBIC, Westwood+, BIC, HTCP) with persistent boot profile saving, and toggle IP forwarding / TTL mangling.
- **Drivers & Modules**: View, load, and manage Wi-Fi, SDR, and serial drivers with sequential loading queue and automated dependency resolution.
- **Memory & MGLRU**: View real-time RAM usage, lock full MGLRU capabilities (`0x0007`), drop caches, and adjust VFS pressure.
- **Process & Activity Log**: Real-time diagnostic stream with execution tracking, one-tap copy, and subsystem telemetry.
- **Reset**: Restore default settings anytime with one tap.

---

## 📱 Tested Device & Compatibility

- **Device**: **Redmi Note 14 4G (`tanzanite`)** / MediaTek Helio G99 (MT6789) family — fully working.
- **OS / ROM**: Xiaomi HyperOS (Android 16).
- **Target Kernel**: Android 16 GKI (`6.12.30-android16`).
- **Stability**: Tested and verified with **SUSFS + NoMount + NetHunter** running together with full cellular and internal Wi-Fi functionality.

---

## 📋 Installation Instructions
<details>
<summary><b>Installation Steps (Click to Expand)</b></summary>
<br>

1. **Prerequisites**:
   - Unlocked bootloader.
   - Backup of your current boot image (`boot.img`).
   - **[Kernel Flasher](https://github.com/fatalcoder524/KernelFlasher/releases)** app.

2. **Flash Kernel & Root**:
   - Download the release bundle (`*-Bundle.zip`) and extract it.
   - Flash `*-AnyKernel3.zip` via **Kernel Flasher**, custom recovery, or **SukiSU Manager**.
   - *(KPM Activation)*: When flashing via SukiSU Manager, selecting **KPM Operation → KPM Patch** injects the KPM payload into the kernel image and activates KPM module support immediately on boot.
   - Install the matching root manager APK (`SukiSU_*.apk`).
   - Reboot device.
   - *(Optional)* Flash **[susfs4ksu-module](https://github.com/sidex15/susfs4ksu-module/releases)** in your root manager for root hiding.

3. **Modules (Optional)**:
   - **NetHunter**: Flash `Nethunter-Wireless-Modules.zip` in your root manager for USB Wi-Fi/SDR drivers and the WebUI manager.
   - **NoMount**: Flash `NoMount-6.12.30-android16-*.zip` in your root manager for stealth VFS root hiding.
   - *Note: Both modules can be flashed and used together without conflicts.*
</details>

---

## 🏆 Credits

- 🏗️ **GKI KernelSU SUSFS**: Based on work by [WildKernels](https://github.com/WildKernels/GKI_KernelSU_SUSFS)
- 🔐 **SukiSU-Nova**: Developed by [SukiSU-Nova](https://github.com/SukiSU-Nova/SukiSU-Nova)
- 🛡️ **SUSFS**: Developed by [simonpunk](https://gitlab.com/simonpunk/susfs4ksu.git)
- 🐉 **Kali NetHunter**: Developed by the [Offensive Security / Kali NetHunter Team](https://www.kali.org/docs/nethunter/)
- 🪝 **NoMount**: Developed by [maxsteeel](https://github.com/maxsteeel/nomount)
- 🛡️ **Baseband-guard**: Developed by [vc-teahouse](https://github.com/vc-teahouse/Baseband-guard)
- 📦 **DroidSpaces-OSS**: Developed by [ravindu644](https://github.com/ravindu644/Droidspaces-OSS)
- 🔌 **USB Arsenal**: Developed by [ravindu644](https://github.com/ravindu644/USB-Arsenal)
- ⚡ **Kernel Flasher**: Developed by [fatalcoder524](https://github.com/fatalcoder524/KernelFlasher)
