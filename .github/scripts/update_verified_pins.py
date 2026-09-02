#!/usr/bin/env python3
"""Promote latest-built commits to the verified pins in .github/config/commits.json.

Update mode: builds happen at latest branch tips. After a successful build run,
if the components built in this run all passed, their resolved SHAs overwrite
the verified pins in commits.json. Previous verified pins are recorded in
.github/pins/history/<date>.json before being replaced.
"""
import json
import os
import re
import sys
from datetime import datetime, timezone

REPO = os.environ.get("GITHUB_WORKSPACE", ".")
COMMITS_JSON = os.path.join(REPO, ".github/config/commits.json")

# Mapping of (json_key, subkey, sha_env_var, approve_env_var)
PINS = [
    ("nomount", "dev", "NOMOUNT_SHA", "APPROVE_NOMOUNT"),
    ("susfs", "gki-android16-6.12", "SUSFS_SHA", "APPROVE_SUSFS"),
    ("kernelsu_next", "dev-susfs", "KERNELSU_NEXT_SHA", "APPROVE_KERNELSU_NEXT"),
    ("sukisu_ultra", "main", "SUKISU_ULTRA_SHA", "APPROVE_SUKISU_ULTRA"),
    ("resukisu", "main", "RESUKISU_SHA", "APPROVE_RESUKISU"),
]

SHA_RE = re.compile(r"^[0-9a-f]{40}$")


def approved(env_var):
    return os.environ.get(env_var, "").strip().lower() in ("1", "true", "yes")


def history_path():
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H%M%SZ")
    d = os.path.join(REPO, ".github/pins/history")
    os.makedirs(d, exist_ok=True)
    return os.path.join(d, f"{ts}.json")


def write_history(old_data, path):
    record = {
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "previous_verified": old_data,
    }
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(record, fh, indent=2)
        fh.write("\n")
    print(f"  history written: {os.path.relpath(path, REPO)}")


def main():
    if not os.path.exists(COMMITS_JSON):
        print(f"Error: {COMMITS_JSON} not found", file=sys.stderr)
        sys.exit(1)

    with open(COMMITS_JSON, "r", encoding="utf-8") as fh:
        data = json.load(fh)

    old_data = json.loads(json.dumps(data))
    changed = False

    for top_key, sub_key, sha_env, approve_env in PINS:
        new_sha = os.environ.get(sha_env, "").strip().lower()
        if not new_sha:
            continue
        if not SHA_RE.match(new_sha):
            print(f"  skip {top_key}.{sub_key}: invalid SHA '{new_sha}'", file=sys.stderr)
            continue
        if not approved(approve_env):
            print(f"  skip {top_key}.{sub_key}: not approved for promotion")
            continue

        current_sha = data.get(top_key, {}).get(sub_key)
        if current_sha == new_sha:
            print(f"  unchanged {top_key}.{sub_key} ({new_sha[:8]})")
            continue

        if top_key not in data:
            data[top_key] = {}
        data[top_key][sub_key] = new_sha
        print(f"  promoted {top_key}.{sub_key}: {current_sha or 'none'} -> {new_sha}")
        changed = True

    if changed:
        hpath = history_path()
        write_history(old_data, hpath)
        with open(COMMITS_JSON, "w", encoding="utf-8") as fh:
            json.dump(data, fh, indent=2)
            fh.write("\n")
        print(f"  commits.json updated successfully.")
    else:
        print("  no pin changes to promote.")


if __name__ == "__main__":
    main()
