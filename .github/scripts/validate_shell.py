#!/usr/bin/env python3

import concurrent.futures
import pathlib
import re
import subprocess
import sys
import yaml

EXCLUDE_DIRS = {".git", ".repo", "out", "bazel-bin", "kernel"}
GHA_EXPR_RE = re.compile(r"\$\{\{\s*[^}]*\s*\}\}")


def find_shell_files(root="."):
    for path in pathlib.Path(root).rglob("*.sh"):
        if any(part in EXCLUDE_DIRS for part in path.parts):
            continue
        yield path


def extract_inline_scripts():
    scripts = []
    yaml_paths = list(pathlib.Path(".github/workflows").glob("*.yml")) + \
                 list(pathlib.Path(".github/workflows").glob("*.yaml")) + \
                 list(pathlib.Path(".github/actions").rglob("action.yml")) + \
                 list(pathlib.Path(".github/actions").rglob("action.yaml"))

    for ypath in yaml_paths:
        try:
            with open(ypath, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
        except Exception:
            continue

        if not isinstance(data, dict):
            continue

        # Check composite action steps
        if "runs" in data and isinstance(data["runs"], dict):
            steps = data["runs"].get("steps", [])
            if isinstance(steps, list):
                for idx, step in enumerate(steps, 1):
                    if isinstance(step, dict) and "run" in step and step.get("shell") in (None, "bash", "sh"):
                        step_name = step.get("name", f"step_{idx}")
                        scripts.append((f"{ypath} -> {step_name}", step["run"]))

        # Check workflow jobs steps
        if "jobs" in data and isinstance(data["jobs"], dict):
            for job_name, job in data["jobs"].items():
                if isinstance(job, dict):
                    steps = job.get("steps", [])
                    if isinstance(steps, list):
                        for idx, step in enumerate(steps, 1):
                            if isinstance(step, dict) and "run" in step and step.get("shell") in (None, "bash", "sh"):
                                step_name = step.get("name", f"step_{idx}")
                                scripts.append((f"{ypath} -> {job_name} -> {step_name}", step["run"]))

    return scripts


def check_file(path):
    result = subprocess.run(
        ["bash", "-n", str(path)],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return str(path), result.stderr.strip()
    return str(path), None


def check_script_content(entry):
    name, content = entry
    # Replace GitHub Actions template expressions with dummy quotes for bash syntax check
    sanitized = GHA_EXPR_RE.sub('"__GHA_EXPR__"', content)
    result = subprocess.run(
        ["bash", "-n"],
        input=sanitized,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return name, result.stderr.strip()
    return name, None


def main():
    files = sorted(find_shell_files())
    inline_scripts = extract_inline_scripts()

    status = 0
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results_files = executor.map(check_file, files)
        for path, error in results_files:
            if error:
                print(f"Syntax error in shell file: {path}")
                print(f"  {error}")
                status = 1

        results_inline = executor.map(check_script_content, inline_scripts)
        for name, error in results_inline:
            if error:
                print(f"Syntax error in inline script: {name}")
                print(f"  {error}")
                status = 1

    total = len(files) + len(inline_scripts)
    print(f"Checked {len(files)} shell file(s) and {len(inline_scripts)} inline shell block(s) ({total} total).")
    return status


if __name__ == "__main__":
    sys.exit(main())
