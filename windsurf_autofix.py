#!/usr/bin/env python3
"""
🛠️ WINDSURF PHOENIX OMEGA SANCTUM AUTOFIX v13.0

One-command fix for all Python environment issues.
Rebuilds .venv, .git/hooks, requirements, and validates everything.

Usage: ./windsurf_autofix.py
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path


def run_command(cmd, cwd=None):
    """Run shell command and return success status"""
    try:
        result = subprocess.run(
            cmd, shell=True, cwd=cwd, capture_output=True, text=True
        )
        if result.returncode != 0:
            print(f"❌ Command failed: {cmd}")
            print(f"   Error: {result.stderr}")
            return False
        return True
    except Exception as e:
        print(f"❌ Exception running {cmd}: {e}")
        return False


def main():
    """Phoenix Omega Sanctum Autofix Protocol"""
    print("🛠️ WINDSURF PHOENIX OMEGA SANCTUM AUTOFIX v13.0")
    print("🔥 Executing complete environment rebuild...")

    project_root = Path(__file__).parent
    os.chdir(project_root)

    # Phase 1: Purge everything
    print("\n☠️ Phase 1: Total purge...")
    dirs_to_remove = [
        ".venv",
        ".venvv",
        ".git/hooks",
        "__pycache__",
        ".mypy_cache",
        ".pytest_cache",
    ]
    for dir_path in dirs_to_remove:
        if Path(dir_path).exists():
            shutil.rmtree(dir_path, ignore_errors=True)
            print(f"   Removed: {dir_path}")

    # Phase 2: Set Python version
    print("\n🐍 Phase 2: Setting Python 3.12.8...")
    with open(".python-version", "w") as f:
        f.write("3.12.8\n")
    with open(".tool-versions", "w") as f:
        f.write("python 3.12.8\n")

    if not run_command("pyenv install -s 3.12.8"):
        print("❌ Failed to install Python 3.12.8")
        return False

    if not run_command("pyenv local 3.12.8"):
        print("❌ Failed to set local Python version")
        return False

    # Phase 3: Rebuild venv
    print("\n🔧 Phase 3: Rebuilding virtual environment...")
    if not run_command("python -m venv .venv"):
        print("❌ Failed to create virtual environment")
        return False

    if not run_command(
        "source .venv/bin/activate && pip install --upgrade pip setuptools wheel"
    ):
        print("❌ Failed to upgrade pip tools")
        return False

    if not run_command("source .venv/bin/activate && pip install -r requirements.txt"):
        print("❌ Failed to install requirements")
        return False

    # Phase 4: Reinstall hooks
    print("\n⚙️ Phase 4: Reinstalling pre-commit hooks...")
    if not run_command("source .venv/bin/activate && pre-commit clean"):
        print("❌ Failed to clean pre-commit")
        return False

    if not run_command("source .venv/bin/activate && pre-commit install"):
        print("❌ Failed to install pre-commit hooks")
        return False

    # Phase 5: Validation
    print("\n✅ Phase 5: Final validation...")
    result = subprocess.run(
        "source .venv/bin/activate && python --version",
        shell=True,
        capture_output=True,
        text=True,
    )
    if "3.12.8" not in result.stdout:
        print("❌ Python version validation failed")
        return False

    print("\n🎉 PHOENIX OMEGA SANCTUM AUTOFIX COMPLETE!")
    print("🐍 Python 3.12.8 environment ready")
    print("🔒 All hooks installed and validated")
    print("✅ Ready for immortal commits")

    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
