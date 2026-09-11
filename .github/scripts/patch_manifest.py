#!/usr/bin/env python3
"""Patch kernel manifest default.xml to pin kernel/common to a specific revision."""
import os
import re
import sys

def main():
    if len(sys.argv) < 3:
        print("Usage: patch_manifest.py <manifest_path> <revision>", file=sys.stderr)
        sys.exit(1)

    manifest_path = sys.argv[1]
    revision = sys.argv[2]

    if not os.path.isfile(manifest_path):
        print(f"ERROR: manifest file not found: {manifest_path}", file=sys.stderr)
        sys.exit(1)

    with open(manifest_path, "r", encoding="utf-8") as f:
        content = f.read()

    pattern = r"(<project\s+path=[\"\x27]common[\"\x27]\s+name=[\"\x27]kernel/common[\"\x27])[^>]*>"
    replacement = f"\\g<1> revision=\"{revision}\">"
    new_content, count = re.subn(pattern, replacement, content)

    if count == 0:
        print(f"WARNING: kernel/common project tag not found in {manifest_path}", file=sys.stderr)
    else:
        with open(manifest_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"Successfully patched {manifest_path}: pinned kernel/common to revision {revision}")

if __name__ == "__main__":
    main()
