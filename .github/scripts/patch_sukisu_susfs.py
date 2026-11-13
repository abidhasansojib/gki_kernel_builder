#!/usr/bin/env python3
"""
Patch SukiSU-Ultra kernel implementation to provide complete SUSFS integration.

This script hooks SukiSU-Ultra with SUSFS (v2.3.0) by:
1. Adding the 'KernelSU - SUSFS' menu with all CONFIG_KSU_SUSFS_* options into drivers/kernelsu/Kconfig.
2. Initializing susfs via susfs_init() in kernelsu_init() in kernel/core/init.c.
3. Adding the ksu_handle_sys_reboot() handler in kernel/supercall/dispatch.c to dispatch SUSFS_MAGIC commands.
4. Exporting and implementing ksu_supercall_reboot_handler() in kernel/supercall/supercall.{c,h}.
5. Implementing SUSFS SELinux domain checks and batch SID registration in kernel/selinux/selinux.{c,h}.
6. Triggering susfs_set_batch_sid() upon SELinux policy application in kernel/selinux/rules.c.
7. Hooking susfs_add_sus_avd_allowed_by_type() and susfs_add_sus_type() in kernel/selinux/sepolicy.c.
8. Triggering susfs_parse_priority_app_strings() upon throne updates in kernel/manager/pkg_observer.c.

All modifications are strictly idempotent and safe to run multiple times.
"""

import argparse
import os
import re
import sys

SUSFS_KCONFIG_SNIPPET = """
menu "KernelSU - SUSFS"
config KSU_SUSFS
	bool "KernelSU addon - SUSFS"
	depends on KSU
	depends on THREAD_INFO_IN_TASK
	default y
	help
	  Patch and Enable SUSFS to kernel with KernelSU.

config KSU_SUSFS_SUS_PATH
	bool "Enable to hide suspicious path"
	depends on KSU_SUSFS
	default y
	help
	  - Allow hiding the user-defined path and all its sub-paths from various system calls.
	  - Use "add_sus_path_loop" instead of "add_sus_path" if the user-defined path is frequently modified.
	  - Use with cautious as it may cause performance loss and will be vulnerable to side channel attacks,
	  	just disable this feature if it doesn't work for you or you don't need it at all.
	  - Effective only on zygote/zygote_next spawned user app process that is marked with TIF_PROC_UMOUNTED.

config KSU_SUSFS_SUS_MOUNT
	bool "Enable to hide suspicious mounts"
	depends on KSU_SUSFS
	default y
	help
	  - Automatically assign fake mnt_id and fake mnt_group_id for mounts mounted by ksu process until
	    /sdcard is  decrypted, this is to evade from mnt_id/mnt_group_id gap detections.
	  - Allow hiding all sus mounts from /proc/self/[mounts|mountinfo|mountstat] for non-su processes.
	  - Effective only on zygote/zygote_next spawned user app process that is marked with TIF_PROC_UMOUNTED.

config KSU_SUSFS_SUS_KSTAT
	bool "Enable to spoof suspicious kstat"
	depends on KSU_SUSFS
	default y
	help
	  - Allow spoofing the kstat of user-defined file/directory.
	  - Effective on all processes with (uid % 100000) >= 10000.

config KSU_SUSFS_SPOOF_UNAME
	bool "Enable to spoof uname"
	depends on KSU_SUSFS
	default y
	help
	  - Allow spoofing the string returned by uname syscall to user-defined string.
	  - Effective on all processes.

config KSU_SUSFS_ENABLE_LOG
	bool "Enable logging susfs log to kernel"
	depends on KSU_SUSFS
	default y
	help
	  - Allow logging susfs log to kernel, uncheck it to completely disable all susfs log.

config KSU_SUSFS_HIDE_KSU_SUSFS_SYMBOLS
	bool "Enable to automatically hide ksu and susfs symbols from /proc/kallsyms"
	depends on KSU_SUSFS
	default y
	help
	  - Automatically hide ksu and susfs symbols from '/proc/kallsyms'.
	  - Effective on all processes.

config KSU_SUSFS_SPOOF_CMDLINE_OR_BOOTCONFIG
	bool "Enable to spoof /proc/bootconfig (gki) or /proc/cmdline (non-gki)"
	depends on KSU_SUSFS
	default y
	help
	  - Spoof the output of /proc/bootconfig (gki) or /proc/cmdline (non-gki) with a user-defined file.
	  - Effective on all processes.

config KSU_SUSFS_OPEN_REDIRECT
	bool "Enable to redirect a path to be opened with another path"
	depends on KSU_SUSFS
	default y
	help
	  - Allow redirecting a target path to be opened with another user-defined path.
	  - Both target path and redirected path must be existed before they can be added to the kernel.
	  - Users have to take care of the selinux permission of both target path and redirected path by themselves.
	  - OPEN_REDIRECT does not bypass some detections by default, but users can work with SUS_KSTAT to bypass them.
	  - Effective only on processes with pre-defined uid scheme.

config KSU_SUSFS_SUS_MAP
	bool "Enable to hide some mmapped real file from different proc maps interfaces"
	depends on KSU_SUSFS
	default y
	help
	  - Allow hiding mmapped real file from /proc/<pid>/[maps|smaps|smaps_rollup|map_files|mem|pagemap]
	  - It does NOT support hiding for anon memory.
	  - It does NOT hide any inline hooks or plt hooks cause by the injected library itself.
	  - It may not be able to evade detections by apps that implement a good injection detection.
	  - Effective only on zygote/zygote_next spawned user app process that is marked with TIF_PROC_UMOUNTED

config KSU_SUSFS_PRIORITY_UID_FILTER
	bool "Enable to allow adding user-defined uids that will be hidden from getpriority/setpriority/ioprio_get/ioprio_set syscall"
	depends on KSU_SUSFS
	default y
	help
	  - Allow hiding user-defined uids from syscalls like getpriority/setpriority/ioprio_get/ioprio_set.
	  - Effective on all processes with uid >= 10000.

endmenu
"""

DISPATCH_REBOOT_HANDLER = """
#ifdef CONFIG_KSU_SUSFS
#include <linux/susfs.h>
int ksu_handle_sys_reboot(int magic1, int magic2, unsigned int cmd, void __user **arg)
{
    if (magic1 != KSU_INSTALL_MAGIC1) {
        return -EINVAL;
    }

    if (magic2 == SUSFS_MAGIC && current_uid().val == 0) {
        switch(cmd) {
#ifdef CONFIG_KSU_SUSFS_SUS_PATH
        case CMD_SUSFS_ADD_SUS_PATH:
            susfs_add_sus_path(arg);
            return 0;
        case CMD_SUSFS_ADD_SUS_PATH_LOOP:
            susfs_add_sus_path_loop(arg);
            return 0;
#endif // #ifdef CONFIG_KSU_SUSFS_SUS_PATH
#ifdef CONFIG_KSU_SUSFS_SUS_MOUNT
        case CMD_SUSFS_HIDE_SUS_MNTS_FOR_NON_SU_PROCS:
            susfs_set_hide_sus_mnts_for_non_su_procs(arg);
            return 0;
#endif // #ifdef CONFIG_KSU_SUSFS_SUS_MOUNT
#ifdef CONFIG_KSU_SUSFS_SUS_KSTAT
        case CMD_SUSFS_ADD_SUS_KSTAT:
            susfs_add_sus_kstat(arg);
            return 0;
        case CMD_SUSFS_UPDATE_SUS_KSTAT:
            susfs_update_sus_kstat(arg);
            return 0;
        case CMD_SUSFS_ADD_SUS_KSTAT_STATICALLY:
            susfs_add_sus_kstat(arg);
            return 0;
#endif // #ifdef CONFIG_KSU_SUSFS_SUS_KSTAT
#ifdef CONFIG_KSU_SUSFS_SPOOF_UNAME
        case CMD_SUSFS_SET_UNAME:
            susfs_set_uname(arg);
            return 0;
#endif // #ifdef CONFIG_KSU_SUSFS_SPOOF_UNAME
#ifdef CONFIG_KSU_SUSFS_ENABLE_LOG
        case CMD_SUSFS_ENABLE_LOG:
            susfs_enable_log(arg);
            return 0;
#endif // #ifdef CONFIG_KSU_SUSFS_ENABLE_LOG
#ifdef CONFIG_KSU_SUSFS_SPOOF_CMDLINE_OR_BOOTCONFIG
        case CMD_SUSFS_SET_CMDLINE_OR_BOOTCONFIG:
            susfs_set_cmdline_or_bootconfig(arg);
            return 0;
#endif // #ifdef CONFIG_KSU_SUSFS_SPOOF_CMDLINE_OR_BOOTCONFIG
#ifdef CONFIG_KSU_SUSFS_OPEN_REDIRECT
        case CMD_SUSFS_ADD_OPEN_REDIRECT:
            susfs_add_open_redirect(arg);
            return 0;
#endif // #ifdef CONFIG_KSU_SUSFS_OPEN_REDIRECT
#ifdef CONFIG_KSU_SUSFS_SUS_MAP
        case CMD_SUSFS_ADD_SUS_MAP:
            susfs_add_sus_map(arg);
            return 0;
#endif // #ifdef CONFIG_KSU_SUSFS_SUS_MAP
#ifdef CONFIG_KSU_SUSFS_PRIORITY_UID_FILTER
        case CMD_SUSFS_SET_PRIORITY_UID_FILTER:
            susfs_set_priority_uid_filter(arg);
            return 0;
#endif // #ifdef CONFIG_KSU_SUSFS_PRIORITY_UID_FILTER
        case CMD_SUSFS_ENABLE_AVC_LOG_SPOOFING:
            susfs_set_avc_log_spoofing(arg);
            return 0;
        case CMD_SUSFS_SHOW_ENABLED_FEATURES:
            susfs_get_enabled_features(arg);
            return 0;
        case CMD_SUSFS_SHOW_VARIANT:
            susfs_show_variant(arg);
            return 0;
        case CMD_SUSFS_SHOW_VERSION:
            susfs_show_version(arg);
            return 0;
        default:
            return -EINVAL;
        }
    }

    if (magic2 == KSU_INSTALL_MAGIC2) {
        return ksu_supercall_reboot_handler(arg);
    }

    return -EINVAL;
}
#endif
"""

SELINUX_SUSFS_DEFS = """
#ifdef CONFIG_KSU_SUSFS
#include <linux/susfs.h>

#define KERNEL_INIT_DOMAIN "u:r:init:s0"
#define KERNEL_ZYGOTE_DOMAIN "u:r:zygote:s0"
#define KERNEL_ZYGOTE_NEXT_DOMAIN "u:r:zygote_next:s0"
#define KERNEL_PRIV_APP_DOMAIN "u:r:priv_app:s0:c512,c768"

u32 susfs_ksu_sid __read_mostly = 0;
u32 susfs_init_sid __read_mostly = 0;
u32 susfs_zygote_sid __read_mostly = 0;
u32 susfs_zygote_next_sid __read_mostly = 0;
u32 susfs_priv_app_sid __read_mostly = 0;

static inline void susfs_set_sid(const char *secctx_name, u32 *out_sid)
{
    int err;
    if (!secctx_name || !out_sid) {
        return;
    }
    err = security_secctx_to_secid(secctx_name, strlen(secctx_name), out_sid);
    if (err) {
        pr_err("failed setting sid for '%s', err: %d\\n", secctx_name, err);
        return;
    }
    pr_info("sid '%u' is set for secctx_name '%s'\\n", *out_sid, secctx_name);
}

bool susfs_is_current_ksu_domain(void) {
    return unlikely(current_sid() == susfs_ksu_sid);
}

bool susfs_is_current_init_domain(void) {
    return unlikely(current_sid() == susfs_init_sid);
}

bool susfs_is_current_zygote_domain(void) {
    return unlikely(current_sid() == susfs_zygote_sid);
}

bool susfs_is_current_zygote_next_domain(void) {
    return unlikely(current_sid() == susfs_zygote_next_sid);
}

void susfs_set_batch_sid(void)
{
    susfs_set_sid(KERNEL_ZYGOTE_DOMAIN, &susfs_zygote_sid);
    susfs_set_sid(KERNEL_ZYGOTE_NEXT_DOMAIN, &susfs_zygote_next_sid);
    susfs_set_sid(KERNEL_SU_CONTEXT, &susfs_ksu_sid);
    susfs_set_sid(KERNEL_INIT_DOMAIN, &susfs_init_sid);
    susfs_set_sid(KERNEL_PRIV_APP_DOMAIN, &susfs_priv_app_sid);
}
#endif
"""

SUPERCALL_REBOOT_HANDLER_C = """
#ifdef CONFIG_KSU_SUSFS
int ksu_supercall_reboot_handler(void __user **arg)
{
    struct ksu_install_fd_tw *tw;

    tw = kzalloc(sizeof(*tw), GFP_KERNEL);
    if (!tw)
        return 0;

    tw->outp = (int __user *)(*arg);
    tw->cb.func = ksu_install_fd_tw_func;

    if (task_work_add(current, &tw->cb, TWA_RESUME)) {
        kfree(tw);
        pr_warn("install fd add task_work failed\\n");
    }

    return 0;
}
#endif
"""


def find_ksu_directory(base_dir):
    candidates = [
        os.path.join(base_dir, "common", "drivers", "kernelsu"),
        os.path.join(base_dir, "drivers", "kernelsu"),
        os.path.join(base_dir, "SukiSU-Ultra", "kernel"),
        os.path.join(base_dir, "SukiSU-Ultra"),
        os.path.join(base_dir, "KernelSU", "kernel"),
        os.path.join(base_dir, "KernelSU"),
        os.path.join(base_dir, "kernel", "common", "drivers", "kernelsu"),
        os.path.join(base_dir, "kernel", "drivers", "kernelsu"),
        os.path.join(base_dir, "kernel", "SukiSU-Ultra", "kernel"),
        os.path.join(base_dir, "kernel", "SukiSU-Ultra"),
        os.path.join(base_dir, "kernel", "KernelSU", "kernel"),
        os.path.join(base_dir, "kernel", "KernelSU"),
        os.path.join(base_dir, "kernel"),
        base_dir,
    ]
    for c in candidates:
        if os.path.isdir(c):
            real = os.path.realpath(c)
            kconfig = os.path.join(real, "Kconfig")
            has_init = (
                os.path.exists(os.path.join(real, "core", "init.c"))
                or os.path.exists(os.path.join(real, "ksu_main.c"))
                or os.path.exists(os.path.join(real, "kernel", "ksu_main.c"))
                or os.path.exists(os.path.join(real, "kernel", "core", "init.c"))
            )
            if os.path.exists(kconfig) and has_init:
                return real
    return None


def patch_kconfig(ksu_dir):
    kconfig_path = os.path.join(ksu_dir, "Kconfig")
    if not os.path.exists(kconfig_path):
        print(f"[WARN] {kconfig_path} not found.")
        return False

    with open(kconfig_path, "r", encoding="utf-8") as f:
        content = f.read()

    if 'menu "KernelSU - SUSFS"' in content:
        print("[INFO] Kconfig already contains KernelSU - SUSFS menu.")
        return True

    idx = content.rfind("endmenu")
    if idx == -1:
        print("[ERROR] Could not find 'endmenu' in Kconfig.")
        return False

    new_content = content[:idx] + SUSFS_KCONFIG_SNIPPET.strip() + "\n\n" + content[idx:]
    with open(kconfig_path, "w", encoding="utf-8") as f:
        f.write(new_content)
    print(f"[INFO] Successfully patched {kconfig_path} with SUSFS Kconfig options.")
    return True


def patch_init_c(ksu_dir):
    path = os.path.join(ksu_dir, "core", "init.c")
    if not os.path.exists(path):
        main_c = os.path.join(ksu_dir, "ksu_main.c")
        if os.path.exists(main_c):
            with open(main_c, "r", encoding="utf-8") as f:
                content = f.read()
            if "susfs_init();" in content:
                print(f"[INFO] {main_c} already calls susfs_init().")
                return True
            if "ksu_init_symbol_resolver();" in content:
                content = "#ifdef CONFIG_KSU_SUSFS\n#include <linux/susfs.h>\n#endif\n" + content
                content = content.replace(
                    "ksu_init_symbol_resolver();",
                    "ksu_init_symbol_resolver();\n\n#ifdef CONFIG_KSU_SUSFS\n    susfs_init();\n#endif",
                    1,
                )
                with open(main_c, "w", encoding="utf-8") as f:
                    f.write(content)
                print(f"[INFO] Successfully patched {main_c} for susfs_init().")
                return True
        print(f"[WARN] Neither {path} nor ksu_main.c found in {ksu_dir}.")
        return False

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    modified = False
    if "#include <linux/susfs.h>" not in content:
        inc = '#ifdef CONFIG_KSU_SUSFS\n#include <linux/susfs.h>\n#endif\n'
        content = inc + content
        modified = True

    if "susfs_init();" not in content:
        target = "ksu_init_symbol_resolver();"
        if target in content:
            replacement = target + "\n\n#ifdef CONFIG_KSU_SUSFS\n    susfs_init();\n#endif"
            content = content.replace(target, replacement, 1)
            modified = True
        else:
            print("[WARN] Could not find 'ksu_init_symbol_resolver();' in core/init.c")

    if modified:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"[INFO] Successfully patched {path} for susfs_init().")
    else:
        print(f"[INFO] {path} is already patched for SUSFS.")
    return True


def patch_supercall_h(ksu_dir):
    path = os.path.join(ksu_dir, "supercall", "supercall.h")
    if not os.path.exists(path):
        print(f"[WARN] {path} not found.")
        return False

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    if "ksu_supercall_reboot_handler" in content:
        print(f"[INFO] {path} already declares ksu_supercall_reboot_handler.")
        return True

    idx = content.rfind("#endif")
    if idx == -1:
        print(f"[ERROR] Could not find #endif in {path}")
        return False

    decl = "\n#ifdef CONFIG_KSU_SUSFS\nint ksu_supercall_reboot_handler(void __user **arg);\n#endif\n\n"
    content = content[:idx] + decl + content[idx:]
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"[INFO] Successfully patched {path} with ksu_supercall_reboot_handler declaration.")
    return True


def patch_supercall_c(ksu_dir):
    path = os.path.join(ksu_dir, "supercall", "supercall.c")
    if not os.path.exists(path):
        print(f"[WARN] {path} not found.")
        return False

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    if "ksu_supercall_reboot_handler" in content:
        print(f"[INFO] {path} already defines ksu_supercall_reboot_handler.")
        return True

    content = content.rstrip() + "\n" + SUPERCALL_REBOOT_HANDLER_C.strip() + "\n"
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"[INFO] Successfully patched {path} with ksu_supercall_reboot_handler definition.")
    return True


def patch_dispatch_c(ksu_dir):
    path = os.path.join(ksu_dir, "supercall", "dispatch.c")
    if not os.path.exists(path):
        print(f"[WARN] {path} not found.")
        return False

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    if "ksu_handle_sys_reboot" in content:
        print(f"[INFO] {path} already contains ksu_handle_sys_reboot.")
        return True

    content = content.rstrip() + "\n" + DISPATCH_REBOOT_HANDLER.strip() + "\n"
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"[INFO] Successfully patched {path} with ksu_handle_sys_reboot.")
    return True


def patch_selinux_h(ksu_dir):
    path = os.path.join(ksu_dir, "selinux", "selinux.h")
    if not os.path.exists(path):
        print(f"[WARN] {path} not found.")
        return False

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    if "susfs_is_current_ksu_domain" in content:
        print(f"[INFO] {path} already declares SUSFS SELinux helpers.")
        return True

    idx = content.rfind("#endif")
    if idx == -1:
        print(f"[ERROR] Could not find #endif in {path}")
        return False

    decls = (
        "\n#ifdef CONFIG_KSU_SUSFS\n"
        "bool susfs_is_current_ksu_domain(void);\n"
        "bool susfs_is_current_init_domain(void);\n"
        "bool susfs_is_current_zygote_domain(void);\n"
        "bool susfs_is_current_zygote_next_domain(void);\n"
        "void susfs_set_batch_sid(void);\n"
        "#endif\n\n"
    )
    content = content[:idx] + decls + content[idx:]
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"[INFO] Successfully patched {path} with SUSFS SELinux declarations.")
    return True


def patch_selinux_c(ksu_dir):
    path = os.path.join(ksu_dir, "selinux", "selinux.c")
    if not os.path.exists(path):
        print(f"[WARN] {path} not found.")
        return False

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    if "susfs_set_batch_sid" in content:
        print(f"[INFO] {path} already defines SUSFS SELinux helpers.")
        return True

    content = content.rstrip() + "\n" + SELINUX_SUSFS_DEFS.strip() + "\n"
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"[INFO] Successfully patched {path} with SUSFS SELinux definitions.")
    return True


def patch_rules_c(ksu_dir):
    path = os.path.join(ksu_dir, "selinux", "rules.c")
    if not os.path.exists(path):
        print(f"[WARN] {path} not found.")
        return False

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    if "susfs_set_batch_sid();" in content:
        print(f"[INFO] {path} already calls susfs_set_batch_sid().")
        return True

    # Target: reset_avc_cache(pol->latest_granting);
    pattern = r"(reset_avc_cache\([^\)]*\);)"
    replacement = r"\1\n\n#ifdef CONFIG_KSU_SUSFS\n    susfs_set_batch_sid();\n#endif"
    content_new, count = re.subn(pattern, replacement, content, count=1)
    if count == 0:
        # Fallback target: before out_unlock: in apply_kernelsu_rules
        if "out_unlock:" in content:
            content_new = content.replace(
                "out_unlock:",
                "#ifdef CONFIG_KSU_SUSFS\n    susfs_set_batch_sid();\n#endif\nout_unlock:",
                1
            )
            count = 1

    if count > 0:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content_new)
        print(f"[INFO] Successfully patched {path} to call susfs_set_batch_sid().")
        return True

    print(f"[ERROR] Could not find insertion point in {path}.")
    return False


def patch_sepolicy_c(ksu_dir):
    path = os.path.join(ksu_dir, "selinux", "sepolicy.c")
    if not os.path.exists(path):
        print(f"[WARN] {path} not found.")
        return False

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    if "susfs_add_sus_avd_allowed_by_type" in content:
        print(f"[INFO] {path} already patched for SUSFS.")
        return True

    # 1. Add externs at top
    externs = (
        "#ifdef CONFIG_KSU_SUSFS\n"
        "extern int susfs_add_sus_avd_allowed_by_type(u32 s_type, u32 t_type, u16 type, u32 orig_avd_allowed);\n"
        "extern int susfs_add_sus_type(const char *secctx, u32 type_value);\n"
        "#endif // #ifdef CONFIG_KSU_SUSFS\n\n"
    )
    content = externs + content

    # 2. In add_rule_raw: after get_avtab_node check
    pattern_rule = (
        r"(node\s*=\s*get_avtab_node\(db,\s*&key,\s*NULL\);\s*\n\s*if\s*\(!node\)\s*\n\s*return\s+false;)"
    )
    replace_rule = (
        r"\1\n\n#ifdef CONFIG_KSU_SUSFS\n"
        r"        susfs_add_sus_avd_allowed_by_type(src->value, tgt->value, cls->value, node->datum.u.data);\n"
        r"#endif // #ifdef CONFIG_KSU_SUSFS"
    )
    content, count_rule = re.subn(pattern_rule, replace_rule, content, count=1)

    # 3. In add_type: after ebitmap_set_bit loop
    pattern_type = (
        r"(ebitmap_set_bit\(&db->role_val_to_struct\[i\]->types,\s*value\s*-\s*1,\s*1\);\s*\n\s*})"
    )
    replace_type = (
        r"\1\n\n#ifdef CONFIG_KSU_SUSFS\n"
        r"    susfs_add_sus_type(type_name, type->value);\n"
        r"#endif // #ifdef CONFIG_KSU_SUSFS"
    )
    content, count_type = re.subn(pattern_type, replace_type, content, count=1)

    if count_rule > 0 and count_type > 0:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"[INFO] Successfully patched {path} for SUSFS avd and types.")
        return True

    print(f"[ERROR] Failed to patch {path}: rule_match={count_rule}, type_match={count_type}")
    return False


def patch_pkg_observer_c(ksu_dir):
    path = os.path.join(ksu_dir, "manager", "pkg_observer.c")
    if not os.path.exists(path):
        print(f"[WARN] {path} not found.")
        return False

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    if "susfs_parse_priority_app_strings" in content:
        print(f"[INFO] {path} already calls susfs_parse_priority_app_strings().")
        return True

    # 1. Include <linux/susfs.h> at top
    inc = "#ifdef CONFIG_KSU_SUSFS_PRIORITY_UID_FILTER\n#include <linux/susfs.h>\n#endif\n"
    content = inc + content

    # 2. In ksu_track_throne_tw_func: after track_throne(false);
    pattern = r"(track_throne\(false\);)"
    replacement = (
        r"\1\n#ifdef CONFIG_KSU_SUSFS_PRIORITY_UID_FILTER\n"
        r"    susfs_parse_priority_app_strings();\n"
        r"#endif"
    )
    content_new, count = re.subn(pattern, replacement, content, count=1)
    if count > 0:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content_new)
        print(f"[INFO] Successfully patched {path} with susfs_parse_priority_app_strings().")
        return True

    print(f"[ERROR] Could not find 'track_throne(false);' in {path}")
    return False


def patch_selinux_hide_c(ksu_dir):
    path = os.path.join(ksu_dir, "feature", "selinux_hide.c")
    if not os.path.exists(path):
        print(f"[INFO] {path} not found, skipping selinux_hide patch.")
        return True

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    modified = False
    if "static bool ksu_selinux_hide_running" in content:
        content = content.replace("static bool ksu_selinux_hide_running", "bool ksu_selinux_hide_running")
        modified = True
    if "static bool ksu_selinux_hide_enabled" in content:
        content = content.replace("static bool ksu_selinux_hide_enabled", "bool ksu_selinux_hide_enabled")
        modified = True

    if modified:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"[INFO] Successfully patched {path} for extern symbol linkage.")
    else:
        print(f"[INFO] {path} already has non-static linkage.")
    return True


def main():
    parser = argparse.ArgumentParser(description="Patch SukiSU-Ultra for native SUSFS integration.")
    parser.add_argument("--kernel-dir", default=".", help="Base kernel directory")
    parser.add_argument("--ksu-dir", default=None, help="Explicit path to SukiSU-Ultra kernel directory")
    args = parser.parse_args()

    ksu_dir = args.ksu_dir
    if not ksu_dir or not os.path.isdir(ksu_dir):
        ksu_dir = find_ksu_directory(args.kernel_dir)

    if not ksu_dir or not os.path.isdir(ksu_dir):
        print(f"[ERROR] Could not locate SukiSU-Ultra directory in '{args.kernel_dir}'.", file=sys.stderr)
        sys.exit(1)

    print(f"[INFO] Found SukiSU-Ultra kernel directory at: {ksu_dir}")

    success = all([
        patch_kconfig(ksu_dir),
        patch_init_c(ksu_dir),
        patch_supercall_h(ksu_dir),
        patch_supercall_c(ksu_dir),
        patch_dispatch_c(ksu_dir),
        patch_selinux_h(ksu_dir),
        patch_selinux_c(ksu_dir),
        patch_rules_c(ksu_dir),
        patch_sepolicy_c(ksu_dir),
        patch_pkg_observer_c(ksu_dir),
        patch_selinux_hide_c(ksu_dir),
    ])

    if not success:
        print("[ERROR] One or more SukiSU-Ultra SUSFS patch operations failed.", file=sys.stderr)
        sys.exit(1)

    print("[SUCCESS] SukiSU-Ultra successfully patched for complete SUSFS integration.")


if __name__ == "__main__":
    main()
