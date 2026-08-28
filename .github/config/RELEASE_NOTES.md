# GKI Kernel Release (6.12.30-android16)

> [!CAUTION]
> This software is provided for testing and educational purposes only. Use at your own risk. Ensure you have backups of your current `boot.img` before installation.

---

## 🔐 Root & Build Metadata

* **Root Solution**: **{{ROOT_IMPL}}**
* **Manager**: {{KSU_MANAGER}}
* **Root Version**: `{{KSU_VERSION}}` (Tag: `{{KSU_GIT_TAG}}`)
* **Branch / Commit**: `{{KSUN_BRANCH}}` (`{{KSUN_COMMIT}}`)
{{SUSFS_BRANCHES}}

---

## ✨ Features Summary

* 🛡️ **[SUSFS v2.2.0](https://gitlab.com/simonpunk/susfs4ksu)**: Advanced kernel-level root hiding & VFS redirection coexistence with NoMount. Recommended module: [susfs4ksu-module by sidex15](https://github.com/sidex15/susfs4ksu-module).
* 🐉 **[Kali NetHunter & Wireless Stack](https://www.kali.org/docs/nethunter/)**: Monitor mode, frame injection (`mac80211`/`cfg80211`), BadUSB HID (`/dev/hidg0`), RTL-SDR, SocketCAN, and 75+ modular USB WiFi drivers.
* 🛡️ **[Baseband Guard (BBG)](https://github.com/vc-teahouse/Baseband-guard)**: LSM protection preventing unauthorized writes to baseband/modem partitions.
* 📦 **[DroidSpaces-OSS](https://github.com/ravindu644/Droidspaces-OSS)**: Container runtime support with SYSVIPC compatibility.
* 🚀 **Networking & Performance**: BBRv3, CAKE Qdisc, WireGuard VPN, IP Set, CIFS/SMB, and NTSync synchronization.

> 📖 *For complete technical details, driver chipsets, and feature matrices, visit the [Project README](https://github.com/abidhasansojib/gki_kernel_builder#readme).*

---

## 📲 Quick Installation Guide

### Prerequisites
* Unlocked bootloader on stock `6.12.30-android16` GKI.
* Backup of stock `boot.img`.
* Flashing tool: [Kernel Flasher](https://github.com/fatalcoder524/KernelFlasher) or Custom Recovery.

### Installation Steps
1. **Flash Kernel**:
   * Open **Kernel Flasher** and flash `*-AnyKernel3.zip` to the active slot.
   * **Xiaomi HyperOS 3 (e.g. Redmi Note 14 4G `tanzanite`)**: Press **Volume Up (`[VOL+]`)** during flashing to install **Bypass-Image** and bypass vendor module CRC verification.
2. **Install Root Manager**:
   * Install the matching Manager app for **{{ROOT_IMPL}}** (KernelSU-Next, SukiSU-Ultra, or ReSukiSU).
3. **Load NetHunter Drivers (Optional)**:
   * Flash `Nethunter-Wireless-Module.zip` in your Root Manager to auto-load external USB WiFi/SDR drivers and firmware.
4. **Reboot** and verify root and features.

---

### 🔍 Verification Direct on Device
Run the automated auditor script in Termux / root shell:
```bash
curl -sSL https://raw.githubusercontent.com/abidhasansojib/gki_kernel_builder/main/checker.sh | su -c "sh"
```
