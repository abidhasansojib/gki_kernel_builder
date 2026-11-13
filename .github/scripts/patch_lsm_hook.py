#!/usr/bin/env python3
"""
patch_lsm_hook.py - Bypass security_add_hooks() for Linux 6.12+ / SUSFS

In Linux 6.12, LSM uses static calls (lsm_static_call) and compile-time fixed
MAX_LSM_COUNT slots. All slots are populated during early boot (security_init).
When SukiSU-Ultra initializes at device_initcall time, calling security_add_hooks()
triggers a kernel panic: "security_add_hooks Too many LSMs registered."

Furthermore, when CONFIG_KSU_SUSFS is enabled, KernelSU's setresuid and credential
hooks are handled directly by SUSFS inline hooks in kernel/sys.c (ksu_handle_setresuid),
rendering security_add_hooks() completely unnecessary.

This script patches ksu_lsm_hook_init() in lsm_hook.c to bypass security_add_hooks()
on Linux 6.12+ and whenever CONFIG_KSU_SUSFS is defined, preventing the bootloop
panic while preserving symbol and hook cleanliness.

Usage:
    python3 patch_lsm_hook.py <path/to/lsm_hook.c>
"""

import re
import sys


def patch(path: str) -> None:
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # Idempotency guard
    if "lsm_hook_init bypassed for Linux 6.12+ / SUSFS" in content:
        print(f"[INFO] {path} already has lsm_hook bypass -- skipping.")
        return

    # Clean up any previously injected ksu_lsm_id declaration
    if "static const struct lsm_id ksu_lsm_id" in content:
        content = re.sub(
            r'#if LINUX_VERSION_CODE >= KERNEL_VERSION\(6, 12, 0\)\s*\n'
            r'static const struct lsm_id ksu_lsm_id\s*=\s*\{[^}]*\};\s*\n'
            r'#endif\s*\n\s*',
            '',
            content,
        )

    # Mark ksu_hooks as __maybe_unused to prevent compiler warning when bypassed
    if "static struct security_hook_list ksu_hooks[] =" in content:
        content = content.replace(
            "static struct security_hook_list ksu_hooks[] =",
            "static struct security_hook_list ksu_hooks[] __maybe_unused =",
        )

    # Locate ksu_lsm_hook_init
    fn_start = content.find("void __init ksu_lsm_hook_init(void)")
    if fn_start == -1:
        print(f"[WARN] ksu_lsm_hook_init not found in {path}.")
        return

    fn_end = content.find("void ksu_lsm_hook_exit(void)", fn_start)
    if fn_end == -1:
        fn_end = content.find("void __exit ksu_lsm_hook_exit(void)", fn_start)

    if fn_end == -1:
        print(f"[WARN] ksu_lsm_hook_exit not found in {path}.")
        return

    new_fn = (
        "void __init ksu_lsm_hook_init(void)\n"
        "{\n"
        "#if LINUX_VERSION_CODE < KERNEL_VERSION(6, 12, 0) && !defined(CONFIG_KSU_SUSFS)\n"
        "#if LINUX_VERSION_CODE >= KERNEL_VERSION(4, 11, 0)\n"
        '    security_add_hooks(ksu_hooks, ARRAY_SIZE(ksu_hooks), "ksu");\n'
        "#else\n"
        "    // https://elixir.bootlin.com/linux/v4.10.17/source/include/linux/lsm_hooks.h#L1892\n"
        "    security_add_hooks(ksu_hooks, ARRAY_SIZE(ksu_hooks));\n"
        "#endif\n"
        "#else\n"
        "    (void)ksu_hooks;\n"
        '    pr_info("ksu: lsm_hook_init bypassed for Linux 6.12+ / SUSFS\\n");\n'
        "#endif\n"
        '    pr_info("LSM hooks initialized.\\n");\n'
        "}\n\n"
    )

    content = content[:fn_start] + new_fn + content[fn_end:]

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"[SUCCESS] Patched {path} to bypass security_add_hooks on Linux 6.12+ / SUSFS.")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <path/to/lsm_hook.c>", file=sys.stderr)
        sys.exit(1)
    patch(sys.argv[1])
