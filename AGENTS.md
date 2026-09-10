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
  * Cloned from `ReSukiSU` main branch (pinned to `3c188288`).
  * **Skips `static.patch`** as ReSukiSU already provides native extern declarations.
  * Configured with `CONFIG_KSU_MULTI_MANAGER_SUPPORT=n` (isolates manager access) and `CONFIG_KSU_TOOLKIT_SUPPORT=y` (enables built-in root toolkit).

### 2. Stealth & Root Hiding Stack
* **SUSFS v2.3.0:**
  * In-tree kernel patches applied to `fs/`, `kernel/`, and `security/` for kernel-level mount isolation, process masking, and symbol hiding. Pinned to latest verified commit `7d91da2d2ce056d1abf378d9199aaf1072d37ab0`.
  * **Unconditional Open Redirect:** `CONFIG_KSU_SUSFS_OPEN_REDIRECT=y` is always enabled, ensuring path redirection works seamlessly alongside NoMount.
* **NoMount VFS Redirection Metamodule:**
  * Pinned to audited commit `d0f57d5c` with SHA-based pre-fetching to withstand upstream `dev` branch rewinds.
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
* **Integrated Material 3 WebUI Dashboard & Action Launcher:**
  * **Module Staging:** `webroot/index.html` (embedded within `Nethunter-Wireless-Modules.zip`).
  * **Root Bridge Execution:** Supports KernelSU (`window.ksu`), APatch, SukiSU-Ultra, and ReSukiSU (`window.suki`). Automatically falls back to safe read-only preview mode when opened in standard web browsers.
  * **Zero Fake Telemetry:** Fully dynamic real-time parsing from kernel filesystems:
    * Available TCP algorithms dynamically queried from `/proc/sys/net/ipv4/tcp_available_congestion_control`.
    * True RAM usage calculated dynamically via $\text{Used} = \text{MemTotal} - \text{MemAvailable}$ from `/proc/meminfo`.
    * MGLRU capabilities inspected from `/sys/kernel/mm/lru_gen/enabled` (with one-tap `0x0007` locking).
    * ZRAM compression algorithm and disk size extracted directly from `/sys/block/zram0/`.
  * **BadUSB HID & Gadget Controller:** ConfigFS integration supporting hotplug toggling between Stock Android USB (MTP + ADB), BadUSB HID Keyboard/Mouse (`/dev/hidg0`, `/dev/hidg1`), USB Mass Storage, and RNDIS Ethernet, including an on-screen DuckyScript test keystroke injector.
  * **Driver Manager:** Dynamic category filtering, multi-tier dependency auto-loading from `lkm/`, and safe reverse-order driver unbinding.
  * **Subsystem Reset Buttons:** One-tap Reset buttons on every view to restore network, USB, driver, and memory parameters back to kernel defaults.
  * **CPU Governor Design:** Intentionally omitted from WebUI per user request; kernel sets `schedutil` as default in `gki_defconfig` and `service.sh`, allowing users to tune governors via FKM.
  * **Storage Mirror & Recovery Resilience:** Auto-synced to `/storage/emulated/0/Download/nethunter_webui.html` both at flash-time (`customize.sh`) and late-boot (`service.sh`) to support TWRP recovery installations.
  * **Safe Action Launcher (`action.sh`):** Launches the WebUI via public storage URI to prevent Android cross-app `ERR_ACCESS_DENIED` errors from `/data/adb`.
* **Single-Storage Packaging (`Nethunter-Wireless-Modules.zip`):**
  * Module ID: `nethunter_wireless_modules` | Name: `Nethunter Wireless,HID Driver & Modules` | Author: `abidhasansojib`.
  * Packaged in a lightweight single `lkm/` storage directory and firmware in `system/etc/firmware/` (reduced ZIP from 52 MB to 14 MB).
  * `post-fs-data.sh`: Dynamically auto-populates firmware paths (`/vendor/firmware`, `/vendor/etc/firmware`, `/system/etc/firmware`) and loads core networking modules early.
  * `service.sh`: Loads all remaining drivers on boot in a 3-pass loop with underscore-hyphen normalization matching `lsmod`, applies native ueventd permissions, enforces `schedutil`, and syncs WebUI.

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

## 🚀 Recent Architecture Improvements & Fixes
* **Pinned Commit Support for Root Flavors:** Passed `matrix.commit` into `kernelsu/action.yml` so `commit_mode: verified` strictly checks out the audited commit SHA instead of branch tips.
* **Isolated Pin Promotion Job:** Moved pin promotion from inside the matrix runner into a post-build `promote-pins` job, eliminating multi-runner git race conflicts and premature promotions.
* **Real Bazel Cache Restoration:** Integrated `actions/cache@v4` in `cache-setup/action.yml` to restore and save `/home/runner/.cache/bazel` across runs.
* **CIFS Input Decoupling:** Removed unconditional CIFS invocation inside `networking/action.yml`, restoring granular control via `use_cifs`.
* **Full Inline Shell Script Validation:** Enhanced `validate_shell.py` to extract all 60+ inline `run:` blocks from workflows and composite actions and validate their syntax via `bash -n`.
* **Heredoc Compliance in FUSE-BPF:** Replaced base64 string dumps with clean, standard heredocs in `fuse-bpf/action.yml`.
* **Stable Zig Compiler Pinning:** Pinned Zig version to `0.13.0` in `nomount-metamodule/action.yml` for CI build stability.
* **Idempotent IPC Symbol Exports:** Protected `EXPORT_SYMBOL_GPL(put_ipc_ns)` and `EXPORT_SYMBOL_GPL(init_ipc_ns)` in `droidspaces/action.yml` against duplicate symbol appends.
* **Automatic Sublevel Detection:** Fixed Makefile sublevel extraction in `extract-sublevel-file-name/action.yml`.
* **Optimized Docker Cache Pruning:** Switched to `docker system prune -af --volumes` in `disk-cleanup/action.yml` to maximize free runner disk space.
* **Patch Rejection Step Summary:** Added rejection count reporting directly into `build-summary` to surface patch collisions immediately.
* **Documentation Alignment:** Updated `docs/ROOT_VARIANTS.md` to reflect unconditional `CONFIG_KSU_SUSFS_OPEN_REDIRECT=y`.
* **Prerequisite Job Early-Abort:** Updated `build-kernel` condition to abort early if `build-nomount-module` fails, saving runner time.
* **Shallow Git Clones:** Added `--depth=1` to dependency clones in `setup-build-environment/action.yml` to minimize bandwidth and checkout latency.
* **Misc BPF Config Decoupling:** Removed duplicate BPF configs from `misc/action.yml` so `use_bpf` maintains strict control.
* **Robust Kernel Branding Script:** Replaced `$d` deletion in `apply-kernel-branding/action.yml` with top-of-file injection to guarantee script integrity.
* **NetHunter WebUI Dynamic Telemetry & Anti-Simulation:** Completely removed mock/simulated data; implemented strict multi-bridge detection (`KernelSU`, `APatch`, `SukiSU-Ultra`, `ReSukiSU`), dynamic `/proc/meminfo` calculation ($Used = Total - Available$), live TCP congestion control discovery, and live MGLRU/ZRAM telemetry.
* **Action Launcher Public Storage Transition:** Fixed `action.sh` invoking `file:///data/adb/...` which caused `ERR_ACCESS_DENIED` in browsers due to mode `0700` permissions on `/data/adb`; redirected to `/storage/emulated/0/Download/nethunter_webui.html` and added operational bridge guidance.
* **Late-Boot WebUI Sync for TWRP Installs:** Integrated automated storage sync into `service.sh` in `nethunter-module/action.yml` to mirror `webroot/index.html` on boot, ensuring recovery-flashed installations have internal storage WebUI mirrors populated once decrypted.
* **RTW88 Silicon Base Module Dependency Resolution:** Added missing base silicon modules (`rtw88_8822c`, `rtw88_8821c`) to the dependency tree for `rtw88_8822cu` and `rtw88_8821cu` in WebUI module loader, preventing symbol resolution errors during insmod.
* **Reverse Iterative Module Unloading:** Enhanced `resetDriversDefaults()` to unload modules in reverse dependency order in an iterative shell loop, eliminating toybox `rmmod` resource busy failures.
* **Workflow Dead Code Elimination:** Cleaned out redundant `touch gki.fragment` step in `build.yml`.

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
