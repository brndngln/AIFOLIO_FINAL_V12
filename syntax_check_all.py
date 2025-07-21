#!/usr/bin/env python3
"""
Batch syntax checker for all Python files in the codebase.
Systematically checks and reports syntax errors.
"""

import os
import subprocess
import sys
from pathlib import Path


def find_python_files(root_dir):
    """Find all Python files recursively, excluding backups and venv."""
    python_files = []
    exclude_dirs = {".backups", "venv", ".venv", "__pycache__", ".git", "node_modules"}

    for root, dirs, files in os.walk(root_dir):
        # Skip excluded directories
        dirs[:] = [d for d in dirs if d not in exclude_dirs]

        # Skip if current path contains excluded patterns
        if any(excl in root for excl in exclude_dirs):
            continue

        for file in files:
            if file.endswith(".py"):
                python_files.append(os.path.join(root, file))
    return python_files


def check_syntax(file_path):
    """Check syntax of a single Python file."""
    try:
        result = subprocess.run(
            [sys.executable, "-m", "py_compile", file_path],
            capture_output=True,
            text=True,
            timeout=30,
        )
        return result.returncode == 0, result.stderr
    except subprocess.TimeoutExpired:
        return False, "Timeout during compilation"
    except Exception as e:
        return False, str(e)


def main():
    root_dir = "/Users/b/--NeuroCore--/AIFOLIO/AIFOLIO_FINAL_V12"
    python_files = find_python_files(root_dir)

    print(f"Found {len(python_files)} Python files to check...")

    passed = []
    failed = []

    for i, file_path in enumerate(python_files, 1):
        rel_path = os.path.relpath(file_path, root_dir)
        print(f"[{i:3d}/{len(python_files):3d}] Checking {rel_path}...", end=" ")

        success, error = check_syntax(file_path)
        if success:
            print("✅ PASS")
            passed.append(rel_path)
        else:
            print("❌ FAIL")
            failed.append((rel_path, error))

    print(f"\n=== SUMMARY ===")
    print(f"✅ Passed: {len(passed)} files")
    print(f"❌ Failed: {len(failed)} files")

    if failed:
        print(f"\n=== FAILED FILES ===")
        for file_path, error in failed:
            print(f"\n{file_path}:")
            print(f"  {error}")

    return len(failed) == 0


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
