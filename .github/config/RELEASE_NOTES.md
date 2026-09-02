# ⚡ Android 16 GKI Kernel (`6.12.30`)

> [!TIP]
> **Quick Start**: Download your desired **`*-Bundle.zip`** below. It contains the flashable kernel, matching Root Manager APK, and companion driver modules all in one package!

---

### 📦 All-in-One Bundle Contents (`*-Bundle.zip`)

| File in Bundle | Purpose | How to Install |
| :--- | :--- | :--- |
| **`*-AnyKernel3.zip`** | Flashable kernel installer with built-in vendor bypass | Flash via [Kernel Flasher](https://github.com/fatalcoder524/KernelFlasher/releases) or Recovery |
| **`*.apk`** | Official matching Root Manager App | Install directly on Android |
| **`Nethunter-Wireless-Modules.zip`** | 75+ USB WiFi, BadUSB HID, SDR & CAN drivers | Flash inside Root Manager |
| **`NoMount-*.zip`** | Root-hiding VFS Metamodule | Flash inside Root Manager |

---

### 🚀 3-Step Installation Guide

1. **Flash Kernel**: Open **[Kernel Flasher](https://github.com/fatalcoder524/KernelFlasher/releases)** (or custom recovery) and flash **`*-AnyKernel3.zip`** to the active slot. *(Vendor module version bypass is baked in automatically)*
2. **Install Manager**: Install the matching **Manager APK** included in your bundle.
3. **Reboot**: Reboot your device and verify root access. Optionally flash **`Nethunter-Wireless-Modules.zip`** or **`NoMount-*.zip`** inside the Manager.

---

### 🔐 Build & Feature Details
* **Target Kernel:** Android 16 GKI (`6.12.30-android16`, Sublevel `30`, OS Patch `2025-07`)
* **Compatibility:** Xiaomi HyperOS 3 & standard Android 16 GKI devices
* **Root Flavor:** {{ROOT_IMPL}} (`{{KSU_VERSION}}`)
* **Stealth Stack:** SUSFS v2.3.0 (`{{SUSFS_BRANCHES}}`) & NoMount VFS Metamodule
* **NetHunter Stack:** BadUSB HID (`/dev/hidg0`), 75+ USB WiFi drivers (`=m`), SDR & SocketCAN
* **Performance Suite:** 17+ in-tree low-overhead memory, caching, and scheduler optimizations

---

### 📜 Commit Changelog
{{CHANGELOG}}
