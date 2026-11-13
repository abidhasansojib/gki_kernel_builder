#!/usr/bin/env python3
"""
patch_lsm_hook.py - Fix security_add_hooks() API for Linux 6.12+

Linux 6.12 changed the signature of security_add_hooks() so that the third
argument is 'const struct lsm_id *lsmid' instead of 'const char *name'.

The SukiSU-Ultra 'builtin' branch still passes the string literal "ksu", which
causes a compiler error on GKI android16-6.12 kernels.

Notice: lsm_hook.c in SukiSU-Ultra is included by ksu_main.c and contains no
#include statements of its own. The struct lsm_id declaration must be placed
immediately before ksu_lsm_hook_init().

Usage:
    python3 patch_lsm_hook.py <path/to/lsm_hook.c>
"""

import sys


def patch(path: str) -> None:
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # Idempotency guard
    if "ksu_lsm_id" in content:
        print(f"[INFO] {path} already has lsm_id patch -- skipping.")
        return

    old_call = 'security_add_hooks(ksu_hooks, ARRAY_SIZE(ksu_hooks), "ksu");'
    if old_call not in content:
        print(
            f"[WARN] Expected security_add_hooks call not found in {path}. "
            "File may already be patched or has changed upstream."
        )
        return

    target_fn = "void __init ksu_lsm_hook_init(void)"
    lsm_id_decl = (
        "#if LINUX_VERSION_CODE >= KERNEL_VERSION(6, 12, 0)\n"
        "static const struct lsm_id ksu_lsm_id = {\n"
        '\t.name = "ksu",\n'
        "\t.id   = 0,\n"
        "};\n"
        "#endif\n\n"
    )

    if target_fn in content:
        content = content.replace(target_fn, lsm_id_decl + target_fn, 1)
    else:
        # Fallback: prepend to beginning of file
        content = lsm_id_decl + content

    new_call = (
        "#if LINUX_VERSION_CODE >= KERNEL_VERSION(6, 12, 0)\n"
        "    security_add_hooks(ksu_hooks, ARRAY_SIZE(ksu_hooks), &ksu_lsm_id);\n"
        "#else\n"
        '    security_add_hooks(ksu_hooks, ARRAY_SIZE(ksu_hooks), "ksu");\n'
        "#endif"
    )
    content = content.replace(old_call, new_call, 1)

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"[SUCCESS] Patched {path} for Linux 6.12+ lsm_id API.")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <path/to/lsm_hook.c>", file=sys.stderr)
        sys.exit(1)
    patch(sys.argv[1])

