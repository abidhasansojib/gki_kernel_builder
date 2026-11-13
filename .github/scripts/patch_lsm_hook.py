#!/usr/bin/env python3
"""
patch_lsm_hook.py - Fix security_add_hooks() API for Linux 6.12+

Linux 6.12 changed the signature of security_add_hooks() so that the third
argument is 'const struct lsm_id *lsmid' instead of 'const char *name'.

The SukiSU-Ultra 'builtin' branch still passes the string literal "ksu", which
causes a compiler error on GKI android16-6.12 kernels.

This script patches lsm_hook.c to:
  1. Add a 'static const struct lsm_id ksu_lsm_id' declaration guarded by
     LINUX_VERSION_CODE >= KERNEL_VERSION(6, 12, 0).
  2. Replace the security_add_hooks(..., "ksu") call with an #ifdef that uses
     &ksu_lsm_id on 6.12+ and falls back to "ksu" on older kernels.

Usage:
    python3 patch_lsm_hook.py <path/to/lsm_hook.c>
"""

import re
import sys


def patch(path: str) -> None:
    with open(path, "r") as f:
        content = f.read()

    # Idempotency guard
    if "ksu_lsm_id" in content:
        print(f"[INFO] {path} already has lsm_id patch -- skipping.")
        return

    # ------------------------------------------------------------------ #
    # 1) Insert the lsm_id struct declaration after the last #include     #
    # ------------------------------------------------------------------ #
    last_include = -1
    for m in re.finditer(r"^#include\s+\S+.*$", content, re.MULTILINE):
        last_include = m.end()

    if last_include == -1:
        print(f"[WARN] No #include found in {path} -- skipping patch.")
        sys.exit(0)

    lsm_id_decl = (
        "\n\n"
        "#if LINUX_VERSION_CODE >= KERNEL_VERSION(6, 12, 0)\n"
        "static const struct lsm_id ksu_lsm_id = {\n"
        "\t.name = \"ksu\",\n"
        "\t.id   = 0,\n"
        "};\n"
        "#endif\n"
    )
    content = content[:last_include] + lsm_id_decl + content[last_include:]

    # ------------------------------------------------------------------ #
    # 2) Replace the security_add_hooks call that passes the string "ksu" #
    # ------------------------------------------------------------------ #
    old_call = 'security_add_hooks(ksu_hooks, ARRAY_SIZE(ksu_hooks), "ksu");'
    new_call = (
        "#if LINUX_VERSION_CODE >= KERNEL_VERSION(6, 12, 0)\n"
        "    security_add_hooks(ksu_hooks, ARRAY_SIZE(ksu_hooks), &ksu_lsm_id);\n"
        "#else\n"
        '    security_add_hooks(ksu_hooks, ARRAY_SIZE(ksu_hooks), "ksu");\n'
        "#endif"
    )

    if old_call not in content:
        print(
            f"[WARN] Expected security_add_hooks call not found in {path}. "
            "File may already be patched or has changed upstream."
        )
        # Not fatal -- maybe the builtin branch already fixed it
        return

    content = content.replace(old_call, new_call, 1)

    with open(path, "w") as f:
        f.write(content)

    print(f"[SUCCESS] Patched {path} for Linux 6.12+ lsm_id API.")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <path/to/lsm_hook.c>", file=sys.stderr)
        sys.exit(1)
    patch(sys.argv[1])
