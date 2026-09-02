# 🤖 AGENTS.md — Developer & AI Agent Guide

## 📌 Project Overview & Architecture
* **Project Name:** `gki_kernel_builder`
* **Target Kernel:** Android 16 GKI (`6.12.30-android16`, Sublevel `30`, OS Patch Level `2025-07`)
* **Primary Build Platform:** **GitHub Actions CI/CD** &mdash; *Notice: The developer's local environment/device does NOT have local compilation toolchains (no Bazel, Clang, or AOSP cross-compilers). All kernel compilation, toolchains, and module packaging are strictly orchestrated in the cloud via GitHub Actions workflows.*
* **Primary Tested Device:** Redmi Note 14 4G (`tanzanite`) on Xiaomi HyperOS 3 (Android 16).

---

## ⚡ Flashing Architecture: Default Vendor Module Version Bypass
> [!IMPORTANT]
> **Vendor Module Version-Check Bypass Baked In:**
> Modern OEM Android 16 skins (especially Xiaomi HyperOS 3, Samsung OneUI, etc.) enforce strict kernel module CRC and sublevel version verification against OEM vendor modules on boot. 
> In this project, the **kernel version-check bypass hack (`bad_version: return 1;`) is applied automatically by default** during compilation.
>
> **How It Works:**
> 1. The build pipeline generates a single, fully bypassed kernel binary: `Image`.
> 2. `Image` is packaged directly into **`*-AnyKernel3.zip`**.
> 3. Flashing in **[Kernel Flasher](https://github.com/fatalcoder524/KernelFlasher/releases)** or Recovery flashes directly without requiring dual images or interactive volume button prompts.

---

## 🛠️ Comprehensive Feature Implementations

### 1. Root Solutions & Coexistence (`root_flavor`)
The project supports 3 independent root implementations with automated patch resolution (strictly NO official KernelSU):
* **KernelSU-Next (`next` / `kernelsu-next`):**
  * Cloned from upstream `dev-susfs` branch.
  * Applied with `static.patch` to convert `static` functions in `selinux_hide.c` to `extern` for seamless coexistence with SUSFS.
* **SukiSU-Ultra (`ultra` / `sukisu-ultra`):**
  * Cloned from `SukiSU-Ultra` main branch.
  * **Skips `static.patch`** and applies native symbol linkage fixes.
* **ReSukiSU (`resukisu`):**
  * Cloned from `ReSukiSU` main branch.
  * **Skips `static.patch`** as ReSukiSU already provides native extern declarations.

### 2. Stealth & Root Hiding Stack
* **SUSFS v2.3.0:**
  * In-tree kernel patches applied to `fs/`, `kernel/`, and `security/` for kernel-level mount isolation, process masking, and symbol hiding. Pinned to latest verified commit `7d91da2d2ce056d1abf378d9199aaf1072d37ab0`.
* **NoMount VFS Redirection Metamodule:**
  * Auto-cloned and compiled with Zig compiler in GitHub Actions to produce architecture-native **`ko-loader-arm64`** and **`ko-loader-arm`** binaries inside `bin/`.

### 3. Automated Root Manager App Fetching
* **`fetch-root-managers` Action & `managers.yml` Workflow:**
  * Automatically fetches official manager APKs for KernelSU-Next, SukiSU-Ultra, or ReSukiSU during the kernel build or via standalone dispatch workflow.
  * Uploads the manager APK artifact directly alongside build releases.

### 4. Kali NetHunter & Penetration Testing Stack
* **BadUSB / Rubber Ducky HID:**
  * Enabled `/dev/hidg0` USB gadget keyboard/mouse emulation for DuckHunter payloads.
* **75+ Modular Wireless WiFi Drivers (`=m`):**
  * **Realtek:** `rtw88` (8822bu, 8822cu, 8821cu, 8723du), `rtl8xxxu` (8188eus, 8192eu), `rtl8187`.
  * **Atheros:** `ath9k_htc` (AR9271 / TP-Link WN722N v1), `carl9170`.
  * **MediaTek / Ralink:** `mt76x2u` (Alfa AWUS036ACM), `mt76x0u` (Alfa AWUS036ACHM), `mt7601u`, `rt2800usb` (Alfa AWUS036NH / RT3070).
* **Software Defined Radio (SDR):**
  * RTL-SDR / RTL2832U (`dvb_usb_rtl28xxu`, `rtl2832_sdr`), HackRF One (`hackrf.ko`), AirSpy (`airspy.ko`), Mirics (`msi2500.ko`).
* **Automotive & Hardware Hacking:**
  * SocketCAN framework (`can.ko`, `can-raw.ko`, `can-bcm.ko`, `vcan.ko`, `slcan.ko`, `peak_usb.ko`, `kvaser_usb.ko`, `ems_usb.ko`).
  * USB Serial dongles: FTDI (`ftdi_sio.ko`), WCH (`ch341.ko`), Silicon Labs (`cp210x.ko`), Prolific (`pl2303.ko`), CDC-ACM.
* **Bluetooth Attacks:**
  * USB Bluetooth dongles via `btusb.ko` with RFCOMM TTY (`rfcomm.ko`), BNEP, and HIDP.
* **Single-Storage Packaging (`Nethunter-Wireless-Modules.zip`):**
  * Module ID: `nethunter_wireless_modules` | Name: `Nethunter Wireless,HID Driver & Modules` | Author: `abidhasansojib`.
  * Packaged in a lightweight single `lkm/` storage directory and firmware in `system/etc/firmware/` (reduced ZIP from 52 MB to 14 MB).
  * `post-fs-data.sh`: Dynamically auto-populates firmware paths (`/vendor/firmware`, `/vendor/etc/firmware`, `/system/etc/firmware`) and loads core networking modules early.
  * `service.sh`: Loads all remaining drivers on boot in a 3-pass loop with underscore-hyphen normalization matching `lsmod`.

### 5. Performance, Networking & Security Enhancements
* **Performance Patch Suite (`performance/action.yml`):**
  * 17+ low-overhead memory, caching, scheduler, and filesystem optimizations (optimized memory operations, memory prefetch, 16-byte clear page alignment, memcmp optimization, cache pressure reduction, F2FS congestion reduction, ext4 commit age increase, wake attempt reductions).
* **Instant Background Disk Cleanup (`disk-cleanup/action.yml`):**
  * Sub-2-second folder relocation into background trash followed by low-priority disowned background purge, speeding up CI builds.
* **Baseband Guard (BBG):** LSM protection module preventing unauthorized writes to radio/modem partitions.
* **DroidSpaces-OSS:** Lightweight container runtime support with SYSVIPC compatibility.
* **BBRv3 & CAKE Qdisc:** Modern TCP congestion control and network packet queuing algorithms.
* **WireGuard & IP Set:** High-speed in-kernel VPN and firewall rule acceleration.
* **NTSync:** Low-latency NT synchronization primitives for high-performance wine/gaming emulation.
* **BTF / eBPF & FUSE-BPF:** In-tree BTF metadata generation, in-kernel eBPF kprobe/uprobe events, and standalone userspace `fuse-bpf-arm64` daemon.

---

## 📦 Build Artifacts Guide
| Artifact | Flash? | Purpose |
|---|---|---|
| `*-Bundle.zip` | 📦 All-in-One Release | Complete root-flavor bundle containing `AnyKernel3.zip`, matching Manager `APK`, NetHunter & NoMount modules |
| `*-AnyKernel3.zip` | ✅ Flash via Recovery / Kernel Flasher | Single flashable kernel image (`Image`) with vendor bypass baked in |
| `Nethunter-Wireless-Modules.zip` | ✅ Flash via Root Manager | USB WiFi, BadUSB HID, SDR, SocketCAN drivers & firmware |
| `NoMount-*.zip` | ✅ Flash via Root Manager | Root-hiding VFS metamodule (ko-loader + nm binaries) |
| `*-Manager.apk` | 📲 Install on Android | Matching Root Manager APK for the selected root flavor |
| `*-Rejects.zip` | ❌ Do NOT flash | Diagnostic only &mdash; shows which patches failed to apply |
| `*-Summary.md` | ❌ Do NOT flash | Build metadata summary (versions, commits, status) |
| `NoMount-Metamodule` | ❌ Internal artifact | Raw metamodule binary, packaged into NoMount zip |

---

## ⚠️ Strict Operational Rules for AI Agents

1. **Zero-Tolerance for Errors & Bootloop Prevention:**
   * Kernel modifications directly affect hardware stability. A bad patch or syntax error will break the build or cause a **device bootloop**.
   * Always verify shell syntax with `bash -n <script>`, validate workflow manifests with `python3 .github/scripts/validate_workflows.py`, and inspect git diffs thoroughly before committing.
2. **Online Research & Upstream Documentation:**
   * When dealing with unfamiliar kernel configs, compiler warnings, upstream symbol deprecations, or toolchain changes, **search the internet and consult official documentation** (kernel.org, AOSP, LLVM Clang, KernelSU/SUSFS repos).
3. **Ask for Clarification When Uncertain:**
   * Never guess or make unverified assumptions about user preferences or critical build settings. **Ask the user first** if anything is ambiguous.
4. **Log Retention:**
   * **NEVER** delete GitHub Actions workflow run logs automatically. Only delete logs when **explicitly commanded** by the user.
5. **Continuous Documentation & AGENTS.md Updates:**
   * Keep `AGENTS.md` continuously updated with all chat decisions, completed milestones, technical fixes, and workflow structural changes.
6. **Workflow & Repository Architecture Constraints:**
   * **Root Flavors:** `KernelSU-Next`, `SukiSU-Ultra`, `ReSukiSU`, `All` (concurrent multi-flavor matrix build) (strictly NO official KernelSU).
   * **Commit Modes:** `verified` (audited pins in `commits.json`), `latest` (branch tips), and `update` (builds latest then auto-promotes pins on success).
   * **Feature Toggles:** Granular boolean checkboxes for `NoMount`, `Baseband Guard`, `Networking`, `DroidSpaces`, `NTSync`, `Ptrace Patch`, `Unicode Fix`, `BPF Stack`, `Performance`, `Kali NetHunter`, `CIFS`, and `Cache`.
   * **Vendor Module Bypass:** Built-in by default as a single bypassed kernel image (`Image`) without requiring a separate bypass checkbox.
   * **NetHunter Module Metadata:** Name must always be `Nethunter Wireless,HID Driver & Modules`, ID `nethunter_wireless_modules`, ZIP `Nethunter-Wireless-Modules.zip`, and author `abidhasansojib`.
   * **Heredocs in Composite Actions:** Always write inline scripts via clean heredocs (`cat << 'EOF' > file`) with 8-space YAML indentation and trailing `sed -i 's/^[[:space:]]*//' file`. Never use base64 encoding.
