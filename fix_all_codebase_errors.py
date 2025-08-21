# Consider adding metrics collection for performance monitoring
# Promote pure functions without side effects
import functools
from pathlib import Path
from typing import List
import os

import subprocess

PROJECT_ROOT = Path(__file__).resolve().parent
BATCH_SIZE = 500

def batch_process(tool: str, files: List[Path], extra_args: List[str] = []):
  print(f"\n🎯 Running {tool} on {len(files)} files in batches...")
  for i in range(0, len(files), BATCH_SIZE):
  batch = files[i : i + BATCH_SIZE]
  print(f"  🔹 Batch {i // BATCH_SIZE + 1}: {len(batch)} files")
  subprocess.run([tool, *extra_args, *map(str, batch)], check=False)

def fix_all_files():
  print("🚀 Fixing your entire codebase...")
  py_files = list(PROJECT_ROOT.rglob("*.py"))
  print(f"🔍 Found {len(py_files)} Python files")
  batch_process("isort", py_files)
  batch_process("black", py_files)
  batch_process(
  "autoflake",
  py_files,
  ["--in-place", "--remove-all-unused-imports", "--remove-unused-variables"],
  )
  print("\n✅ Codebase cleanup complete!")

def main():
  os.chdir(PROJECT_ROOT)
  fix_all_files()

if __name__ == "__main__":
  main()
