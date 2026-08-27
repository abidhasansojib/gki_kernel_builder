# 🤖 AGENTS.md — Developer & AI Agent Guide

## 📌 Project Overview
* **Repository:** `gki_kernel_builder`
* **Target Kernel:** Android 16 GKI (`6.12.30-android16`, 2025-07 patch level)
* **Tested Device:** Redmi Note 14 4G (`tanzanite`) on Xiaomi HyperOS 3.0.302 (Android 16)
* **Core Integrations:**
  * **Root Solutions:** KernelSU-Next, official KernelSU, and ReSukiSU
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
   * Integrated automated cloning and Zig compilation of **`ko-loader-arm64`** and **`ko-loader-arm`** into `bin/` inside `NoMount-*.zip` (`8e47a8a`).
3. **Diagnostics & Checker Audit (`checker.sh`):**
   * Updated `check_config` in `checker.sh` to match `.ko` binary names against `lsmod` (e.g. `ch341`, `r8152`, `hackrf`, `asix`, `btusb`), ensuring active modules accurately display as `[ ✔ MODULE (LOADED) ]`.
   * Corrected the Realtek RTL8822CU firmware path check to `rtw88/rtw8822c_fw.bin`, achieving 100% firmware presence verification.
4. **Clean Kernel Flags Hardening:**
   * Added fallback bot git credentials (`github-actions[bot]`) in `clean-kernel-flags/action.yml` to prevent commit failures on unconfigured runners.
5. **Issue Templates & Documentation Overhaul:**
   * Redesigned `bug_report.yml` into a structured, field-specific form (Device Name, OS/Android Version, Stock Kernel, Flashed Version, Bypass Flash Mode verification checkbox, Steps to Reproduce, Logs/Screenshots).
   * Removed legacy `dev_use_only.yml`.
   * Updated `README.md` with raw GitHub URL for real-time `checker.sh` execution.
6. **Repository Clean State:**
   * Purged previous release `r1`, remote/local release tags, and 12 past GitHub Actions workflow run logs for a clean baseline.
7. **CI/CD & UI Streamlining:**
   * Streamlined `build.yml` from fragmented matrix jobs into a single direct first-class job (`Build Kernel (6.12.30-android16)`), eliminating the "Show all jobs (1)" UI dropdown in GitHub Actions.
   * Removed `os_patch_level` input and permanently locked the build target to `2025-07` (`6.12.30-android16-2025-07`).
   * Simplified `feature_set` input to 3 clear, clean options: `FULL` (All features + NetHunter), `WITHOUT-NETHUNTER` (Root, SUSFS, NoMount, BBG, NET, DS), and `NONE` (Vanilla stock GKI).

---

### 📋 What's Next (Upcoming Priorities)
1. **Trigger Fresh Kernel Build:**
   * Run the `Build Kernel` workflow via GitHub Actions (`Release` or `Action`) with `FULL` feature set and `KernelSU-Next` to generate the new release assets with all latest patches.
2. **Live Device Verification:**
   * **NoMount:** Flash newly generated `NoMount-*.zip` in KernelSU-Next and confirm clean installation without KoLoader error.
   * **NetHunter Modules:** Verify in-kernel DVB-USB v2 modules and hardware LED blinking triggers on OTG connection.
   * **Checker:** Run `checker.sh` on device to verify all checks pass.
3. **Upstream Monitoring & Maintenance:**
   * Track upstream KernelSU-Next, SUSFS v2.2.0, and NoMount commits for future Android 16 GKI revisions.

---

## 🛠️ Repository Architecture & Key Directories
* `.github/workflows/build.yml` — Main Bazel/Kleaf build pipeline with multi-flavor matrix.
* `.github/workflows/validate.yml` — Static YAML, shell script (`bash -n`), and Python syntax validator.
* `.github/actions/` — Modular composite actions for kernel patching (SUSFS, NoMount, NetHunter, BBG, BBRv3, etc.).
* `checker.sh` — On-device diagnostic shell script for auditing live NetHunter kernel configs and loaded DLKM modules.
* `README.md` & `docs/ROOT_VARIANTS.md` — Project and root variant documentation.
