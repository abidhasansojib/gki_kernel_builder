#!/usr/bin/env python3
"""
Patch Android GKI drivers/usb/gadget/configfs.c to support multiple USB gadgets.

On Android, gadgets_make() calls android_device_create() which attempts to register
an Android USB device ("android%d") in sysfs. Because Android init already creates
the primary system gadget "g1" (occupying /sys/class/android_usb/android1), any
subsequent gadget creation (e.g. gadgetfs, Stryker, BadUSB) fails with -EEXIST.
configfs.c then masks -EEXIST with -ENOMEM ("Out of memory").

This patch allows non-system gadgets (anything other than g1/g0) to bypass
android_device_create, while ensuring gadgets_drop safely checks whether
android_opts.dev is non-NULL before destroying it.
"""

import os
import re
import sys


def patch_configfs(cfg_path):
    if not os.path.exists(cfg_path):
        print(f"[WARN] {cfg_path} not found.")
        return False

    with open(cfg_path, "r", encoding="utf-8") as f:
        content = f.read()

    if "Allow secondary / third-party gadgets" in content:
        print(f"[INFO] {cfg_path} is already patched for multi-gadget support.")
        return True

    pattern_make = (
        r"([ \t]*)if\s*\(\s*android_device_create\(&gi->cdev\.android_opts\)\s*\)\s*"
        r"goto\s+out_free_driver_name_and_function;"
    )
    replace_make = (
        r"\1/*\n"
        r"\1 * Allow secondary / third-party gadgets (e.g. GadgetFS, Stryker, BadUSB)\n"
        r"\1 * to create independent folders without colliding with Android system\n"
        r"\1 * uevent device 'android1' (-EEXIST) which turns into false -ENOMEM.\n"
        r"\1 */\n"
        r'\1if (!strcmp(name, "g1") || !strcmp(name, "g0")) {\n'
        r"\1\tif (android_device_create(&gi->cdev.android_opts))\n"
        r"\1\t\tgoto out_free_driver_name_and_function;\n"
        r"\1} else {\n"
        r"\1\tmemset(&gi->cdev.android_opts, 0, sizeof(gi->cdev.android_opts));\n"
        r"\1}"
    )

    pattern_drop = r"([ \t]*)android_device_destroy\(&gi->cdev\.android_opts\);"
    replace_drop = (
        r"\1if (gi->cdev.android_opts.dev)\n"
        r"\1\tandroid_device_destroy(&gi->cdev.android_opts);"
    )

    content_new, count_make = re.subn(pattern_make, replace_make, content)
    content_new, count_drop = re.subn(pattern_drop, replace_drop, content_new)

    if count_make > 0 and count_drop > 0:
        with open(cfg_path, "w", encoding="utf-8") as f:
            f.write(content_new)
        print(
            f"[INFO] Successfully patched {cfg_path} "
            f"(gadgets_make: {count_make}, gadgets_drop: {count_drop})"
        )
        return True

    print(
        f"[ERROR] Pattern mismatch in {cfg_path}: "
        f"make matches={count_make}, drop matches={count_drop}"
    )
    return False


def main():
    target_path = "drivers/usb/gadget/configfs.c"
    if len(sys.argv) > 1:
        target_path = sys.argv[1]

    if not os.path.exists(target_path):
        candidates = [
            target_path,
            os.path.join("kernel", "common", target_path),
            os.path.join("common", target_path),
        ]
        for cand in candidates:
            if os.path.exists(cand):
                target_path = cand
                break

    if not patch_configfs(target_path):
        print("[WARN] Could not patch configfs.c automatically.")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
