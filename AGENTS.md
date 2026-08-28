# 🤖 AGENTS.md — Developer & AI Agent Guide

## 📌 Project Overview
* **Repository:** `gki_kernel_builder`
* **Target Kernel:** Android 16 GKI (`6.12.30-android16`, 2025-07 patch level)
* **Tested Device:** Redmi Note 14 4G (`tanzanite`) on Xiaomi HyperOS 3.0.302 (Android 16)
* **Core Integrations:**
  * **Root Solutions:** KernelSU-Next (default), SukiSU-Ultra, and ReSukiSU
  * **Stealth & Root Hiding:** SUSFS v2.2.0 & NoMount VFS redirection metamodule
  * **Penetration Testing:** Kali NetHunter (BadUSB HID, USB WiFi drivers, SDR, SocketCAN, Bluetooth, NFS/CIFS)
  * **Performance & Hardening:** BBRv3, CAKE Qdisc, WireGuard, Baseband Guard (BBG), DroidSpaces-OSS, NTSync

---

## 🏃 Current Sprint & Active State

### ✅ What We Did (Completed)
1. **NetHunter & Wireless Driver Enhancements:**
   * Added `CONFIG_DVB_USB_V2=m`, `CONFIG_DVB_CORE=m`, and `CONFIG_DVB_DYNAMIC_MINORS=y` to enable in-kernel DVB-T / RTL-SDR demodulator modules (`dvb-usb-rtl28xxu.ko`, `rtl2832_sdr.ko`, etc.).
   * Enabled hardware LED triggers (`CONFIG_LEDS_CLASS=y`, `CONFIG_LEDS_TRIGGERS=y`, `CONFIG_RTW88_LEDS=y`, `CONFIG_CAN_LEDS=y`).
   * Added POSIX ACL support for NFS (`CONFIG_NFS_V3_ACL=y`, `CONFIG_NFSD_V3_ACL=y`).
   * Cleaned out duplicate legacy aliases (`CONFIG_USB_NET_RTL8152`/`8150`).
2. **NoMount Metamodule Packaging Fix:**
   * Diagnosed and resolved the KernelSU-Next installation failure (`! KoLoader binary not found for architecture: arm64`).
   * Integrated automated cloning and Zig compilation of **`ko-loader-arm64`** and **`ko-loader-arm`** into `bin/` inside `NoMount-*.zip`.
3. **Diagnostics & Checker Audit (`checker.sh`):**
   * Updated `check_config` in `checker.sh` to match `.ko` binary names against `lsmod` (e.g. `ch341`, `r8152`, `hackrf`, `asix`, `btusb`), ensuring active modules accurately display as `[ ✔ MODULE (LOADED) ]`.
   * Corrected the Realtek RTL8822CU firmware path check to `rtw88/rtw8822c_fw.bin`, achieving 100% firmware presence verification.
4. **Clean Kernel Flags Hardening:**
   * Added fallback bot git credentials (`github-actions[bot]`) in `clean-kernel-flags/action.yml` to prevent commit failures on unconfigured runners.
5. **Issue Templates & Documentation Overhaul:**
   * Redesigned `bug_report.yml` into a structured, field-specific form.
   * Removed legacy `dev_use_only.yml`.
   * Updated `README.md` with raw GitHub URL for real-time `checker.sh` execution.
6. **CI/CD & Modular Workflow Architecture:**
   * Restored the clear, modular multi-job workflow graph: **`Resolve NoMount Commit`**, **`Build NoMount Metamodule`**, **`Build Kernel (6.12.30-android16)`**, **`Consolidated Build Summary`**, and **`Publish Release`**.
   * Promoted `build-kernel` to a direct first-class job (no matrix dropdown nesting — shows all jobs directly in Actions UI).
   * Removed `os_patch_level` input — permanently locked to `2025-07`.
   * Simplified `feature_set` to 3 options only: `FULL`, `WITHOUT-NETHUNTER`, `NONE`.
7. **NetHunter Module Metadata & Lightweight Single-Storage Packaging:**
   * Module name: `Nethunter Wireless,HID & Driver Modules` | Author: `abidhasansojib`.
   * **Single-Storage Architecture (`lkm/`):** Eliminated multi-folder `.ko` duplication across `vendor/lib/modules` and `vendor_dlkm/`. All 75+ drivers are packaged once in `lkm/` and firmware once in `system/etc/firmware/`, shrinking the ZIP from ~52 MB down to ~14 MB and device storage footprint from ~143 MB down to ~36 MB.
   * **Smart Dynamic Loader:** `post-fs-data.sh` dynamically detects and populates active device firmware paths (`/vendor/firmware`, `/vendor/etc/firmware`, `/system/etc/firmware`) and loads core networking dependencies early. `service.sh` loads all remaining modules in a 3-pass loop with hyphen-to-underscore translation (`tr '-' '_'`) matching `lsmod`.
   * Added `customize.sh` for rich flashing UI in KernelSU-Next / SukiSU-Ultra / ReSukiSU manager.
8. **`static.patch` Restoration & Linker Fix (`selinux_hide.c`):**
   * **Root Cause of Build Failure (Run `33063924512`):** Removing `static.patch` caused the linker to fail with `undefined symbol: security_context_to_sid_with_policy`, `security_sid_to_context_with_policy`, and `security_compute_av_user_with_policy` because upstream `KernelSU-Next` still forward-declared those functions as `static` in `kernel/feature/selinux_hide.c` (giving them internal linkage), while SUSFS in `security/selinux/selinuxfs.c` called them as `extern`.
   * **Dual-Layer Fix:** Restored `static.patch` at `.github/actions/kernelsu/patches/static.patch` AND added dual-layer `sed` regex replacement in `kernelsu/action.yml` and `build.yml` (`s/^static int security_context_to_sid_with_policy/int security_context_to_sid_with_policy/g`, etc.) with automatic `.rej` cleanup. This guarantees external symbol visibility and produces zero rejects across all root variants.
9. **CI Validator Enhancement:**
   * Expanded `validate_workflows.py` to also parse and validate all **46 composite action YAML manifests** in `.github/actions/`, catching action.yml YAML parse errors on every push before a real build is triggered.
10. **Linux 6.12 (Android 16 GKI) NetHunter Compatibility Audit & Refinement:**
    * Performed on-device diagnostic audit of `checker.sh` (145 checks) against live kernel `6.12.30-android16`.
    * **Obsolete / Inactive Upstream Symbols Cleaned:** Removed `CONFIG_USB_ZD1201` and `CONFIG_USB_NET_RNDIS_WLAN` (removed in Linux 6.8+), `CONFIG_NFSD_V3` (integrated into `CONFIG_NFSD=y`), `CONFIG_USB_SERIAL_CONSOLE=y`, `CONFIG_RTW88_LEDS`, and inactive DVB subdrivers (`CONFIG_DVB_USB_RTL28XXU`, `CONFIG_DVB_RTL2830`, `CONFIG_DVB_RTL2832`, `CONFIG_DVB_RTL2832_SDR`, `CONFIG_DVB_SI2168`).
    * **Modern LED Trigger Standard:** Migrated deprecated `CONFIG_CAN_LEDS` to `CONFIG_LEDS_TRIGGER_NETDEV=y` (`netdev` trigger for CAN/network activity).
    * **Demodulator Auto-Pruning Alignment:** Kept explicit checks for active DVB components `CONFIG_DVB_CORE`, `CONFIG_DVB_USB_V2`, and `CONFIG_DVB_ZD1301_DEMOD`.
    * **Module & Firmware Instructions:** Confirmed that `[ ● MODULE (=m) ]` and `[ ● NOT FOUND / UNLOADED ]` firmware states resolve automatically upon flashing `Nethunter-Wireless-Module.zip` in KernelSU-Next / SukiSU-Ultra / ReSukiSU.

---

### 📋 What's Next (Upcoming Priorities)
1. **Trigger a Fresh Kernel Build:**
   * Run `Build Kernel` workflow with `FULL` feature set + `KernelSU-Next` to produce the updated kernel and `Nethunter-Wireless-Module.zip` with zero rejects and updated DVB/LED drivers.
2. **Live Device Verification:**
   * **Kernel Flash:** Flash the newly built `*-AnyKernel3.zip` via Recovery / Kernel Flasher.
   * **NetHunter Modules:** Flash `Nethunter-Wireless-Module.zip` in KernelSU-Next Manager to load all 75 modular drivers and place all 11 firmware blobs.
   * **Checker:** Run `checker.sh` on device and confirm 100% pass rate.
3. **Upstream Monitoring & Maintenance:**
   * Track upstream KernelSU-Next (`dev-susfs`), SUSFS v2.2.0, and NoMount (`dev`) commits for future Android 16 GKI revisions.

---

## 🛠️ Repository Architecture & Key Directories
* `.github/workflows/build.yml` — Main kernel build pipeline (5 modular jobs: resolve-nomount, build-nomount-module, build-kernel, summary, release).
* `.github/workflows/validate.yml` — Static YAML + shell script (`bash -n`) + Python syntax validator (runs on every push).
* `.github/actions/` — 46 modular composite actions (SUSFS, NoMount, NetHunter, BBG, BBRv3, NTSync, kernelsu, etc.).
* `.github/actions/nethunter-module/action.yml` — Builds & packages the Nethunter Wireless,HID & Driver Modules zip using heredocs (no base64).
* `.github/actions/kernelsu/action.yml` — Downloads & configures KernelSU-Next / SukiSU-Ultra / ReSukiSU. Stale static.patch removed.
* `.github/scripts/validate_workflows.py` — Validates both workflows and all action manifests on every commit.
* `checker.sh` — On-device diagnostic script for auditing live NetHunter kernel configs and loaded DLKM modules.
* `README.md` & `docs/ROOT_VARIANTS.md` — Project and root variant documentation.

---

## 📦 Build Artifacts Guide
| Artifact | Flash? | Purpose |
|---|---|---|
| `*-AnyKernel3.zip` | ✅ Flash via Recovery / Kernel Flasher | Kernel image (Normal + Bypass Image for HyperOS 3) |
| `Nethunter-Wireless-Module.zip` | ✅ Flash via KSU Manager | USB WiFi, BadUSB HID, SDR, SocketCAN drivers & firmware |
| `NoMount-*.zip` | ✅ Flash via KSU Manager | Root-hiding VFS metamodule (ko-loader + nm binaries) |
| `*-Rejects.zip` | ❌ Do NOT flash | Diagnostic only — shows which patches failed to apply |
| `*-Summary.md` | ❌ Do NOT flash | Build metadata summary (versions, commits, status) |
| `NoMount-Metamodule` | ❌ Internal artifact | Raw metamodule binary, packaged into NoMount zip |

---

## ⚠️ Operational Rules for AI Agents
* **Log Retention:** **NEVER** delete GitHub Actions workflow run logs automatically. Only delete logs when **explicitly commanded** by the user.
* **Documentation Integrity:** Preserve all existing comments and docstrings across files unless instructed otherwise.
* **No Matrix Jobs:** Do NOT use `strategy: matrix:` in `build.yml` — the single `build-kernel` job must remain a direct first-class job so all jobs are visible directly in the GitHub Actions UI without any "Show all jobs" dropdown.
* **No `os_patch_level` Input:** The patch level is permanently locked to `2025-07`. Do not add it back as a workflow input.
* **Feature Set Options:** Only 3 allowed: `FULL`, `WITHOUT-NETHUNTER`, `NONE`. Do not add more options without user approval.
* **NetHunter Module Name:** Always `Nethunter Wireless,HID & Driver Modules`. Author: `abidhasansojib`. Do not change without user approval.
* **Heredocs in action.yml:** When writing shell scripts inline in composite actions, always use `cat << 'EOF' > file` style heredocs with proper 8-space YAML indentation + trailing `sed -i 's/^[[:space:]]*//' file` to strip indent. Never use base64-encoded strings.
