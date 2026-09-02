# GKI Kernel Release (6.12.30-android16)

> [!CAUTION]
> This kernel is built exclusively for devices running **Android 16 GKI (`6.12.30-android16`)**. Ensure you have a backup of your stock `boot.img` before installation.

---

## 🔐 Root & Build Metadata

* **Root Solution**: **{{ROOT_IMPL}}**
* **Root Version**: `{{KSU_VERSION}}` (Tag: `{{KSU_GIT_TAG}}`)
* **Branch / Commit**: `{{KSUN_BRANCH}}` (`{{KSUN_COMMIT}}`)
* **SUSFS Branch**: `{{SUSFS_BRANCHES}}`

---

## 📜 Commit Changelog

{{CHANGELOG}}

---

## 📥 Required Downloads & Tools

* **Kernel Flashing Tool**: [Download Kernel Flasher](https://github.com/fatalcoder524/KernelFlasher/releases)
* **SUSFS Module**: [Download susfs4ksu-module (by sidex15)](https://github.com/sidex15/susfs4ksu-module/releases)

> [!NOTE]
> **Root Manager App**: The official matching Root Manager APK is already bundled directly inside your downloaded release package (`*-Bundle.zip`).

---

## 📲 Installation Instructions

### ⚠️ Step 1: Verify Kernel Version
Before flashing, open **Settings $\to$ About Phone $\to$ Android Version** and verify that your device's stock kernel is based on **`6.12.30-android16`**.

### ⚡ Step 2: Flash Kernel
1. Open **[Kernel Flasher](https://github.com/fatalcoder524/KernelFlasher/releases)** (or your custom recovery).
2. Select and flash **`*-AnyKernel3.zip`** to the active slot (vendor module version bypass is baked in automatically).

### 📱 Step 3: Install Manager App & SUSFS
* Install the matching **Root Manager APK** extracted from your downloaded release bundle (`*-Bundle.zip`).
* Flash **[susfs4ksu-module](https://github.com/sidex15/susfs4ksu-module/releases)** in your Root Manager to activate kernel-level root hiding.

### 🔌 Step 4: Load NetHunter Drivers (Optional)
* Flash **`Nethunter-Wireless-Modules.zip`** in your Root Manager to auto-load external USB WiFi, SDR, BadUSB HID, and SocketCAN drivers and firmware.

### 🔄 Step 5: Reboot
* Reboot your device and verify root access in your manager app.
