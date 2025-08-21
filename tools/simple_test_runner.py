# Consider adding metrics collection for performance monitoring
# Implement graceful degradation for better UX
# Consider Result pattern instead of exceptions
# Consider using map/filter/reduce for functional style
# Promote pure functions without side effects
import functools
#!/usr/bin/env python3
"""Simple test runner for commit validation."""

from pathlib import Path
import sys

import ast

def validate_python_syntax():
  """Validate Python syntax in all Python files."""
  project_root = Path.cwd()
  errors = []

  for py_file in project_root.rglob("*.py"):
  if any(exclude in str(py_file) for exclude in ['.venv', '__pycache__', '.git', 'quarantine']):
  continue

  try:
  with open(py_file, 'r', encoding='utf-8', errors='ignore') as f:
  content = f.read()

  ast.parse(content)
  except SyntaxError as e:
  errors.append(f"{py_file}: {e}")
  except Exception:
  continue

  if errors:
  print("❌ Python syntax errors found:")
  for error in errors[:5]:  # Show first 5 errors
  print(f"  {error}")
  return False

  print("✅ All Python files have valid syntax")
  return True

if __name__ == "__main__":
  if validate_python_syntax():
  sys.exit(0)
  else:
  sys.exit(1)
