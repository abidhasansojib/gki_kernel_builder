#!/usr/bin/env python3
"""Trim or verify SukiSU-Ultra's manager table to its own official signing key.

SukiSU-Ultra verifies manager certificates to authorize root manager privileges:
1. Native upstream format: Directly enforces EXPECTED_SIZE and EXPECTED_HASH
   (configured in kernel/Kbuild as KSU_EXPECTED_SIZE=0x35c and
   KSU_EXPECTED_HASH=947ae944... for com.sukisu.ultra).
2. Multi-key table format: In certain forks or legacy/extended versions, an
   apk_sign_keys[] array contains multiple community signing keys.

This script ensures that only SukiSU-Ultra's official manager signing key is
authorized:
- If a multi-key apk_sign_keys[] table is present, it trims it to keep strictly
  the SukiSU-Ultra key and drops all other community keys.
- If native direct-hash checking is present, it verifies and enforces that
  Kbuild and apk_sign.c strictly lock down to SukiSU-Ultra's official key.

Usage:  trim_sukisu_managers.py <path-to-SukiSU-Ultra-checkout>
"""

import os
import re
import sys
from typing import NoReturn

SUKISU_CERT_SIZE = "0x35c"
SUKISU_HASH = "947ae944f3de4ed4c21a7e4f7953ecf351bfa2b36239da37a34111ad29993eef"
SUKISU_PACKAGE = "com.sukisu.ultra"

ROW_RE = re.compile(
    r'^(?P<indent>\s*)'
    r'(?P<braces>\{\s*(?:0x[0-9a-fA-F]+|\d+)\s*,\s*"[0-9a-fA-F]{64}"(?:[^\}]*)\})'
    r'\s*,?\s*'
    r'(?P<comment>//\s*(?P<name>\S+))?\s*$'
)
TABLE_START_RE = re.compile(r"apk_sign_keys\[\]\s*=\s*\{\s*$")


def fail(msg: str) -> NoReturn:
    sys.exit(f"ERROR: {msg}")


def table_bounds(lines: list[str], what: str) -> tuple[int, int]:
    starts = [i for i, ln in enumerate(lines) if TABLE_START_RE.search(ln)]
    if len(starts) != 1:
        fail(f"{what}: expected exactly one apk_sign_keys[] table, found {len(starts)}")
    start = starts[0]
    for i in range(start + 1, len(lines)):
        if lines[i].strip().startswith("}"):
            return start, i
    fail(f"{what}: could not find the closing brace of apk_sign_keys[]")


def main() -> None:
    if len(sys.argv) != 2:
        fail("usage: trim_sukisu_managers.py <path-to-SukiSU-Ultra-checkout>")

    base = sys.argv[1].rstrip("/")
    candidate_paths = [
        os.path.join(base, "kernel", "manager", "apk_sign.c"),
        os.path.join(base, "manager", "apk_sign.c"),
    ]
    path = None
    for cp in candidate_paths:
        if os.path.isfile(cp):
            path = cp
            break

    if not path:
        fail(f"cannot find apk_sign.c under {base} (tried {candidate_paths})")

    try:
        lines = open(path, encoding="utf-8").read().split("\n")
    except OSError as exc:
        fail(f"cannot read {path}: {exc}")

    starts = [i for i, ln in enumerate(lines) if TABLE_START_RE.search(ln)]

    if len(starts) == 0:
        # Upstream native single-manager format (EXPECTED_SIZE / EXPECTED_HASH)
        text = "\n".join(lines)
        if "is_manager_apk" not in text:
            fail("is_manager_apk() not found in apk_sign.c")
        if "EXPECTED_HASH" not in text or "EXPECTED_SIZE" not in text:
            fail("apk_sign.c does not reference EXPECTED_HASH / EXPECTED_SIZE")

        candidate_kbuild_paths = [
            os.path.join(base, "kernel", "Kbuild"),
            os.path.join(base, "Kbuild"),
        ]
        kbuild_path = next((kp for kp in candidate_kbuild_paths if os.path.isfile(kp)), None)
        if kbuild_path:
            try:
                ktext = open(kbuild_path, encoding="utf-8").read()
            except OSError as exc:
                fail(f"cannot read {kbuild_path}: {exc}")

            changed = False
            if SUKISU_HASH not in ktext:
                if re.search(r"KSU_EXPECTED_HASH\s*\??=", ktext):
                    ktext = re.sub(
                        r"KSU_EXPECTED_HASH\s*\??=.*",
                        f"KSU_EXPECTED_HASH ?= {SUKISU_HASH}",
                        ktext,
                    )
                    changed = True
                else:
                    fail(f"{kbuild_path} does not define KSU_EXPECTED_HASH")

            if SUKISU_CERT_SIZE not in ktext:
                if re.search(r"KSU_EXPECTED_SIZE\s*\??=", ktext):
                    ktext = re.sub(
                        r"KSU_EXPECTED_SIZE\s*\??=.*",
                        f"KSU_EXPECTED_SIZE ?= {SUKISU_CERT_SIZE}",
                        ktext,
                    )
                    changed = True
                else:
                    fail(f"{kbuild_path} does not define KSU_EXPECTED_SIZE")

            if changed:
                try:
                    open(kbuild_path, "w", encoding="utf-8").write(ktext)
                except OSError as exc:
                    fail(f"cannot write {kbuild_path}: {exc}")
                print(f"Enforced official SukiSU key in {kbuild_path}")

        print(
            f"SukiSU-Ultra native single manager configuration verified: "
            f"size {SUKISU_CERT_SIZE}, hash {SUKISU_HASH} ({SUKISU_PACKAGE}); "
            f"no array trimming required."
        )
        return

    if len(starts) > 1:
        fail(f"pre-write: expected at most one apk_sign_keys[] table, found {len(starts)}")

    start, end = table_bounds(lines, "pre-write")
    rows = [i for i in range(start + 1, end) if ROW_RE.match(lines[i])]
    if len(rows) < 1:
        fail(f"expected at least 1 certificate row in {path}, found {len(rows)}")

    keep = [i for i in rows if SUKISU_HASH in lines[i]]
    if len(keep) != 1:
        fail(f"expected exactly one SukiSU row ({SUKISU_HASH[:8]}...), found {len(keep)}")

    m = ROW_RE.match(lines[keep[0]])
    if m is None:
        fail("internal error: SukiSU row did not match its own pattern")

    indent = m.group("indent")
    braces = m.group("braces")
    comment = m.group("comment")
    kept_row = f"{indent}{braces}," + (f" {comment}" if comment else "")

    out: list[str] = []
    dropped = 0
    for i, ln in enumerate(lines):
        if i == keep[0]:
            out.append(kept_row)
        elif i in rows:
            dropped += 1
        else:
            out.append(ln)
    text = "\n".join(out)
    try:
        open(path, "w", encoding="utf-8").write(text)
    except OSError as exc:
        fail(f"cannot write {path}: {exc}")

    # Re-read and verify before declaring success.
    check = open(path, encoding="utf-8").read().split("\n")
    cstart, cend = table_bounds(check, "post-write")
    remaining = [i for i in range(cstart + 1, cend) if ROW_RE.match(check[i])]
    if len(remaining) != 1:
        fail(f"post-write check: expected 1 row, found {len(remaining)}")
    if SUKISU_HASH not in check[remaining[0]]:
        fail("post-write check: the surviving row is not the SukiSU key")
    if "is_manager_apk" not in text:
        fail("post-write check: is_manager_apk() disappeared")

    print(
        f"SukiSU manager table trimmed: {len(rows)} rows -> 1 (dropped {dropped}); "
        f"kept size {SUKISU_CERT_SIZE} {check[remaining[0]].strip()}"
    )


if __name__ == "__main__":
    main()
