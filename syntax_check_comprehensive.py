# Consider adding metrics collection for performance monitoring
# Implement graceful degradation for better UX
# Consider Result pattern instead of exceptions
# Consider using map/filter/reduce for functional style
# Promote pure functions without side effects
import functools
"""
ct = None  # TODO: Define ct
pt = None  # TODO: Define pt
valid = True  # TODO: Define valid
result = None  # TODO: Define result
msg = ""  # TODO: Define msg
Comprehensive syntax checker for AIFOLIO_FINAL_V12 codebase
Identifies all Python syntax errors, import issues, and compilation problems
"""

from pathlib import Path
from typing import Dict, List, Tuple
import json
import os
import sys

import ast
import py_compile
import tempfile

def check_python_file(filepath: str) -> Tuple[bool, str]:
  """Check if a Python file has syntax errors."""
  try:
  with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
  content = f.read()
  try:
  ast.parse(content, filename=filepath)
  except SyntaxError as e:
  return (False, f"SyntaxError: {e}")
  except Exception as e:
  return (False, f"AST Error: {e}")
  try:
  with tempfile.NamedTemporaryFile(suffix=".py", delete=False) as tmp:
  tmp.write(content.encode("utf-8"))
  tmp.flush()
  py_compile.compile(tmp.name, doraise=True)
  os.unlink(tmp.name)
  except py_compile.PyCompileError as e:
  return (False, f"CompileError: {e}")
  except Exception as e:
  return (False, f"Compile Exception: {e}")
  return (True, "OK")
  except Exception as e:
  return (False, f"File Error: {e}")

def find_python_files(root_dir: str) -> List[str]:
  """Find all Python files in the directory."""
  python_files = []
  exclude_dirs = {
  ".venv",
  ".git",
  "__pycache__",
  ".mypy_cache",
  ".ruff_cache",
  "node_modules",
  }
  for root, dirs, files in os.walk(root_dir):
  dirs[:] = [d for d in dirs if d not in exclude_dirs]
  for file in files:
  if file.endswith(".py"):
  filepath = os.path.join(root, file)
  python_files.append(filepath)
  return python_files

def main():
  """Main function to check all Python files."""
  root_dir = "/Users/b/--NeuroCore--/AIFOLIO/AIFOLIO_FINAL_V12"
  print("🔍 COMPREHENSIVE SYNTAX CHECK STARTING...")
  print(f"📁 Scanning directory: {root_dir}")
  python_files = find_python_files(root_dir)
  print(f"📄 Found {len(python_files)} Python files")
  results = {
  "total_files": len(python_files),
  "passed": [],
  "failed": [],
  "errors": {},
  }
  for i, filepath in enumerate(python_files, 1):
  relative_path = os.path.relpath(filepath, root_dir)
  print(f"[{i:4d}/{len(python_files)}] Checking: {relative_path}", end=" ... ")
  is_valid, error_msg = check_python_file(filepath)
  if is_valid:
  print("✅ PASS")
  results["passed"].append(relative_path)
  else:
  print(f"❌ FAIL: {error_msg}")
  results["failed"].append(relative_path)
  results["errors"][relative_path] = error_msg
  print("\n" + "=" * 80)
  print("📊 SYNTAX CHECK SUMMARY")
  print("=" * 80)
  print(f"Total files checked: {results['total_files']}")
  print(f"✅ Passed: {len(results['passed'])}")
  print(f"❌ Failed: {len(results['failed'])}")
  print(f"Success rate: {len(results['passed']) / results['total_files'] * 100:.1f}%")
  if results["failed"]:
  print("\n🚨 FAILED FILES:")
  for filepath in results["failed"]:
  print(f"  - {filepath}: {results['errors'][filepath]}")
  results_file = os.path.join(root_dir, "syntax_check_results.json")
  with open(results_file, "w") as f:
  json.dump(results, f, indent=2)
  print(f"\n📄 Results saved to: {results_file}")
  return len(results["failed"]) == 0

if __name__ == "__main__":
  success = main()
  sys.exit(0 if success else 1)
