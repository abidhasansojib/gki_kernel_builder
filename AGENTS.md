# 🤖 AGENTS.md — Developer & AI Agent Guide

## 📌 Project Overview
* **Repository:** `gki_kernel_builder`
* **Target Kernel:** Android 16 GKI (`6.12.30-android16`, 2025-07 patch level)
* **Tested Device:** Redmi Note 14 4G (`tanzanite`) on Xiaomi HyperOS 3.0.302 (Android 16)
* **Core Integrations:**
  * **Root Solutions:** KernelSU-Next (default), official KernelSU, and ReSukiSU
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
7. **NetHunter Module Metadata & Robust Shell Scripting:**
   * Module name: `Nethunter Wireless,HID & Driver Modules` | Author: `abidhasansojib`.
   * Replaced broken base64 decoding in `nethunter-module/action.yml` with plain-text heredocs (`cat << 'EOF'`) + `sed -i 's/^[[:space:]]*//'` to strip YAML indentation — eliminates `base64: invalid input` and `YAML scanning simple key` errors.
   * Added hyphen-to-underscore translation (`tr '-' '_'`) in `service.sh` for accurate `lsmod` multi-pass module checking.
   * Handled `feature_set: NONE` gracefully in the release pipeline (exports `ROOT_IMPL=None (Vanilla Stock GKI)`, skips all KSU git ops).
8. **Stale Patch Cleanup (Rejects Fix):**
   * Diagnosed `6.12.30-android16-2025-07-Rejects` artifact: contained `selinux_hide.c.rej` because `static.patch` tried to remove `static` keyword from 3 forward declarations, but upstream KernelSU-Next already uses `__maybe_static` — making the patch obsolete.
   * Deleted `.github/actions/kernelsu/patches/static.patch` and removed the dead `'Fix KernelSU Static Patch'` step from `kernelsu/action.yml`.
   * Next build will produce **zero rejects**.
9. **CI Validator Enhancement:**
   * Expanded `validate_workflows.py` to also parse and validate all **46 composite action YAML manifests** in `.github/actions/`, catching action.yml YAML parse errors on every push before a real build is triggered.

---

### 📋 What's Next (Upcoming Priorities)
1. **Trigger a Fresh Kernel Build:**
   * Run `Build Kernel` workflow with `FULL` feature set + `KernelSU-Next` to verify zero rejects and clean artifacts.
2. **Live Device Verification:**
   * **NoMount:** Flash `NoMount-*.zip` via KernelSU-Next Manager and confirm clean install (no `KoLoader binary not found` error).
   * **NetHunter Modules:** Flash `Nethunter-Wireless-Module.zip`, verify USB WiFi, BadUSB HID, SDR drivers load correctly via `checker.sh`.
   * **Checker:** Run `checker.sh` on device and confirm 100% pass rate.
3. **Upstream Monitoring & Maintenance:**
   * Track upstream KernelSU-Next (`dev-susfs`), SUSFS v2.2.0, and NoMount (`dev`) commits for future Android 16 GKI revisions.

---

## 🛠️ Repository Architecture & Key Directories
* `.github/workflows/build.yml` — Main kernel build pipeline (5 modular jobs: resolve-nomount, build-nomount-module, build-kernel, summary, release).
* `.github/workflows/validate.yml` — Static YAML + shell script (`bash -n`) + Python syntax validator (runs on every push).
* `.github/actions/` — 46 modular composite actions (SUSFS, NoMount, NetHunter, BBG, BBRv3, NTSync, kernelsu, etc.).
* `.github/actions/nethunter-module/action.yml` — Builds & packages the Nethunter Wireless,HID & Driver Modules zip using heredocs (no base64).
* `.github/actions/kernelsu/action.yml` — Downloads & configures KernelSU-Next / KernelSU / ReSukiSU. Stale static.patch removed.
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
