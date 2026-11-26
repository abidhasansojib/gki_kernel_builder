#!/usr/bin/env python3
"""Trim SukiSU-Nova's manager table in apk_sign.c to its own official signing key.

SukiSU-Nova hardcodes seven trusted manager certificates in
kernel/manager/apk_sign.c:

    static struct apk_sign_key { unsigned size; const char *sha256; }
    apk_sign_keys[] = {
        { 0x35c, "947ae944…" },  // SukiSU
        { 0x396, "f415f4ed…" },  // RKSU
        { 0x033b, "c371061b…" }, // KSU
        { 0x381, "52d52d8c…" },  // WKSU
        { 0x375, "484fcba6…" },  // KowSU
        { 0x3e6, "79e59011…" },  // KSUN
        { 384,   "7e0c6d72…" },  // MKSU
    };

`is_manager_apk()` returns true on the first row that matches, so all seven are
trusted equally. Trimming the table to the single official SukiSU key ensures
only the official SukiSU-Nova Manager APK is trusted by the kernel.

Idempotent: safe to call when already trimmed to the single SukiSU key.
Usage: trim_sukisu_managers.py <path-to-apk_sign.c-or-checkout>
"""

import os
import re
import sys
from typing import NoReturn

SUKISU_CERT_SIZE = "0x35c"
SUKISU_HASH = "947ae944f3de4ed4c21a7e4f7953ecf351bfa2b36239da37a34111ad29993eef"

ROW_RE = re.compile(
    r'^(?P<indent>\s*)'
    r'(?P<braces>\{\s*(?:0x[0-9a-fA-F]+|\d+)\s*,\s*"[0-9a-fA-F]{64}"\s*\})'
    r'\s*,?\s*'
    r'(?P<comment>//\s*(?P<name>\S+))?\s*$'
)
TABLE_START_RE = re.compile(r"apk_sign_keys\[\]\s*=\s*\{\s*$")


def fail(msg: str) -> NoReturn:
    sys.exit(f"ERROR: {msg}")


def resolve_apk_sign_path(arg: str) -> str:
    target = arg.rstrip("/")
    if os.path.isfile(target):
        return target
    for rel in ("kernel/manager/apk_sign.c", "manager/apk_sign.c", "apk_sign.c"):
        candidate = os.path.join(target, rel)
        if os.path.isfile(candidate):
            return candidate
    fail(f"cannot locate apk_sign.c under {arg}")


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
        fail("usage: trim_sukisu_managers.py <path-to-apk_sign.c-or-checkout>")

    path = resolve_apk_sign_path(sys.argv[1])
    try:
        with open(path, encoding="utf-8") as fh:
            lines = fh.read().split("\n")
    except OSError as exc:
        fail(f"cannot read {path}: {exc}")

    start, end = table_bounds(lines, "pre-write")
    rows = [i for i in range(start + 1, end) if ROW_RE.match(lines[i])]
    if not rows:
        fail(f"no certificate rows found in {path}")

    keep = [i for i in rows if SUKISU_HASH in lines[i]]
    if len(keep) != 1:
        fail(f"expected exactly one SukiSU row ({SUKISU_HASH[:8]}...), found {len(keep)} in {path}")

    if len(rows) == 1:
        print(f"[INFO] SukiSU manager table already trimmed to 1 row in {path}")
        return

    m = ROW_RE.match(lines[keep[0]])
    if m is None:
        fail("internal error: SukiSU row did not match its own pattern")
    kept_row = f"{m.group('indent')}{m.group('braces')}," + (
        f" {m.group('comment')}" if m.group("comment") else ""
    )

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
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)

    with open(path, encoding="utf-8") as fh:
        check = fh.read().split("\n")
    cstart, cend = table_bounds(check, "post-write")
    remaining = [i for i in range(cstart + 1, cend) if ROW_RE.match(check[i])]
    if len(remaining) != 1:
        fail(f"post-write check: expected 1 row, found {len(remaining)}")
    if SUKISU_HASH not in check[remaining[0]]:
        fail("post-write check: the surviving row is not the SukiSU key")
    if "is_manager_apk" not in text:
        fail("post-write check: is_manager_apk() disappeared")

    print(
        f"[INFO] SukiSU manager table trimmed: {len(rows)} rows -> 1 (dropped {dropped}); "
        f"kept size {SUKISU_CERT_SIZE} {check[remaining[0]].strip()}"
    )


if __name__ == "__main__":
    main()
