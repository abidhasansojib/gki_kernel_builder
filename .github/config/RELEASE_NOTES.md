# GKI Kernel Release #

**IMPORTANT DISCLAIMER**

> [!CAUTION]
> This software is provided for testing and educational purposes only. Use at your own risk. The developers are not responsible for any damage, data loss, or issues that may occur. Please ensure you have proper backups before installation.

# Features
- [Root Solution ({{ROOT_IMPL}})](#root-solution)
- [SUSFS v2.2.0](#susfs-v220)
- [Kali NetHunter & Wireless Drivers](#kali-nethunter--wireless-drivers)
- [Baseband Guard (BBG)](#baseband-guard-bbg)
- [DroidSpaces-OSS](#droidspaces-oss)
- [Networking Improvements](#networking)
- [NTSync](#ntsync)
- [Misc](#misc)

<!-- NOTE: The anchor links above match GitHub's auto-generated heading IDs (derived from heading text). Do NOT add explicit {#id} heading attributes: GitHub's release-notes renderer does not support them and renders them as literal text. -->

## Root Solution

Integrated root solution: **{{ROOT_IMPL}}** (KernelSU-Next, KernelSU, or ReSukiSU).

Manager: {{KSU_MANAGER}}

> [!IMPORTANT]
> For best compatibility ensure your Manager Version and Kernel Version match eg. 30100 = 30100.

**Version**  
`{{KSU_VERSION}}`

**Tag**  
`{{KSU_GIT_TAG}}`

**Branch**  
`{{KSUN_BRANCH}}`

**Commit**  
`{{KSUN_COMMIT}}`

## [SUSFS v2.2.0](https://gitlab.com/simonpunk/susfs4ksu)

A KSU addon for hiding root using kernel patches and a userspace module!

Recommended Module: [susfs4ksu-module by sidex15](https://github.com/sidex15/susfs4ksu-module)

- SUS_PATH - Hide suspicious paths: hides the user-defined path and all its sub-paths from various system calls. Use `add_sus_path_loop` instead of `add_sus_path` if the path is frequently modified. Caution: may cause performance loss and is vulnerable to side-channel attacks. Effective only on zygote-spawned user app processes with uid >= 10000
- SUS_MOUNT - Hide suspicious mounts (no CLI support): assigns fake mnt_id/mnt_group_id to mounts mounted by the ksu process until /sdcard is decrypted (evades mnt_id/mnt_group_id gap detections), and hides all sus mounts from `/proc/self/[mounts|mountinfo|mountstat]` for non-su processes
- SUS_KSTAT - Spoof kernel statistics: spoofs the kstat of user-defined files/directories. Effective only on zygote-spawned user app processes with uid >= 10000
- SPOOF_UNAME - Kernel version spoofing: spoofs the string returned by the uname syscall to a user-defined string. Effective on all processes
- ENABLE_LOG - Susfs kernel logging: logs susfs events to the kernel log; uncheck to completely disable all susfs log
- HIDE_KSU_SUSFS_SYMBOLS - Hide ksu/susfs symbols: automatically hides ksu and susfs symbols from `/proc/kallsyms`. Effective on all processes
- SPOOF_CMDLINE_OR_BOOTCONFIG - Boot parameter spoofing: spoofs the output of `/proc/bootconfig` (GKI) or `/proc/cmdline` (non-GKI) with a user-defined file. Effective on all processes
- OPEN_REDIRECT - File access redirection: redirects a target path to be opened with another user-defined path (both paths must exist before they can be added). Does NOT bypass detections by itself; SELinux permissions for both paths are the user's responsibility. Effective only on processes with a pre-defined uid scheme
- SUS_MAP - Memory mapping protection: hides mmapped real files from `/proc/<pid>/[maps|smaps|smaps_rollup|map_files|mem|pagemap]`. No anon-memory support; does not hide inline/PLT hooks caused by the injected library itself; may not evade strong injection detection. Effective only on zygote-spawned unmounted user app processes with uid >= 10000
- AVC_SPOOF - Spoof procfs avc denial logs (enabled at runtime via the sidex15 module — not a build-time Kconfig option)

{{SUSFS_BRANCHES}}

## [Kali NetHunter & Wireless Drivers](https://www.kali.org/docs/nethunter/)

Full kernel support for penetration testing and external wireless dongles:
- **Monitor Mode & Packet Injection**: Enabled natively via `mac80211` and `cfg80211`.
- **BadUSB / HID Gadgets**: USB HID Keyboard and Mouse emulation support (`/dev/hidg0`).
- **External USB WiFi Drivers**: Realtek (`rtw88`, `rtl8xxxu`, `rtl8187`), Atheros (`ath9k_htc`, `carl9170`), MediaTek (`mt76`), and Ralink (`rt2800usb`).
- **USB Ethernet Adapters**: CDC-ECM, CDC-NCM, RTL8152, and ASIX AX88179.
- **Bluetooth RFCOMM & SDR**: Native RFCOMM TTY and RTL2832U DVB SDR support.
- **Flashable Module**: Flash the accompanying `Nethunter-Wireless-Module.zip` module in KernelSU/Magisk for plug-and-play driver and firmware auto-loading.

## [Baseband Guard (BBG)](https://github.com/vc-teahouse/Baseband-guard)

A lightweight LSM (Linux Security Module) for the Android kernel, designed to block unauthorized writes to critical partitions/device nodes at the system level.

## [DroidSpaces-OSS](https://github.com/ravindu644/Droidspaces-OSS)

A lightweight, LXC-inspired container runtime for Android and Linux. Run full Linux distributions natively with zero performance penalty.

## Networking

- BBRv1 - Improved TCP congestion control
- BBRv3 - Improved TCP congestion control for Android 16 (6.12)
- Wireguard - Built-in VPN support
- IP Set & IPv6 NAT Support - Advanced firewall capabilities
- TTL Target Support - Network packet manipulation
- CAKE, fq, fq_codel - Traffic shaping and fair queuing for reduced lag and balanced bandwidth
- connmark - Connection marking for packet classification
- TCP congestion control - CUBIC, BIC, Westwood, and HTCP for optimized performance across different network conditions
- CIFS - Network filesystem support (SMB/CIFS sharing)

## Other Features

- TMPFS_XATTR - Extended attributes for tmpfs (Mountify support)
- TMPFS_POSIX_ACL - POSIX ACLs for tmpfs

## [NTSync](#ntsync)

Provide high-performance, low-latency synchronization primitives compatible with the Windows NT kernel API

## [Misc](#misc)

- Unicode Fix: Prevent path traversal and other detections using non-printable Unicode codepoints [Experimental]
- BTF/eBPF Support: CONFIG_BTF, CONFIG_BPF_EVENTS, CONFIG_FUSE_BPF for debugging and eBPF tooling
- TMPFS_XATTR: Extended attributes for tmpfs (Mountify support)
- TMPFS_POSIX_ACL: POSIX ACLs for tmpfs

## Recommended Tools

[Kernel Flasher](https://github.com/fatalcoder524/KernelFlasher)
- Recommended flashing utility

[PixelFlasher by badabing2005](https://github.com/badabing2005/PixelFlasher)
- Pixel phone flashing GUI utility with features.

## Installation Instructions

### Prerequisites
- Unlocked bootloader.
- Backup your current boot image.
- Have root access using Magisk / KernelSU / Apatch (Any forks).

### Via Kernel Flasher
Download the correct AnyKernel3 ZIP for your device.
If you previously used another root method, clean it up first:
a. Magisk: perform a complete uninstall after flashing the AnyKernel3 ZIP.
b. KSU LKM (boot/init_boot/vendor_boot‑patched): Flash back the stock boot/init_boot/vendor_boot depending on what you patched.
c. KSU GKI: if you are 100% sure you already flashed stock init_boot/boot/vendor_boot, no action is needed; otherwise, follow the same steps as KSU LKM.
d. APatch: remove /data/adb contents to avoid leftover root conflicts after flashing the AnyKernel3 ZIP.
Flash the ZIP to the active slot using Kernel Flasher.
Install the KernelSU‑Next Manager APK, same version as mentioned in the release notes.
Open the KernelSU‑Next app.
Reboot the device if you performed any cleanup in step 2

## 📱 Tested Devices & Compatibility

> [!TIP]
> **Universal GKI Compatibility**: Because this is a Generic Kernel Image (GKI), you can flash it on **any Android device running on a kernel based on `6.12.30-android16`** (sublevel 30 / 2025-07 patch level).

| Device | Codename | Tested OS Version | Stock Kernel Version | Flashing Mode | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Redmi Note 14 4G** | `tanzanite` | **Xiaomi HyperOS 3.0.302** (Android 16) | `6.12.30-android16-5-g6e872b4863d6-ab13847919-4k` | **Bypass Image** (`do.flash_bypass=1`) | ✅ Fully Working |

> [!CAUTION]
> **CRITICAL FLASHING WARNINGS**:
> 1. **HyperOS 3.0+ Only**: Do **NOT** flash on HyperOS versions lower than 3.0 (e.g., HyperOS 1.0 or 2.0 based on Android 14/15). Flashing an Android 16 kernel on older Android OS builds will cause a **HARD BRICK**!
> 2. **Must Use Bypass-Image on HyperOS**: You **MUST** set `do.flash_bypass=1` in `anykernel.sh` inside the `AnyKernel3.zip`. Flashing standard `Image` on HyperOS 3 will cause a **bootloop / soft brick** due to vendor module CRC version checks.

## Force Load Kernel Modules (Bypass) — flashing with `Bypass-Image`

> [!IMPORTANT]
> This option replaces the kernel image used during flashing for compatibility workarounds.

**How to enable:**
- Set `do.flash_bypass=1` in the `anykernel.sh` file within `AnyKernel3.zip`. 

**Behavior:**
- If `do.flash_bypass=1` is set, it will flash `Bypass-Image` (with vendor module CRC check bypass) instead of standard `Image`.
- If `do.flash_bypass=1` is set and `Bypass-Image` is not found, the installer will abort with an error.

**Why / When to use:**
- **Required for Xiaomi HyperOS 3** (such as Redmi Note 14 4G / `tanzanite`) and any OEM builds that enforce strict vendor module version validation.
