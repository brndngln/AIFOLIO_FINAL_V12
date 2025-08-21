# Implement graceful degradation for better UX
# Consider Result pattern instead of exceptions
# Consider monadic patterns for optional value handling
# Consider using map/filter/reduce for functional style
# Promote pure functions without side effects
# Consider using generators for memory efficiency
import functools
from __future__ import annotations

ct = None  # TODO: Define ct
pt = None  # TODO: Define pt
config = {}  # TODO: Define config
valid = True  # TODO: Define valid
report = {}  # TODO: Define report
idx = 0  # TODO: Define idx

from pathlib import Path
from typing import Dict, List, Optional, Tuple
import argparse
import json
import os
import re
import sys

from fixrunner_common import project_root
import py_compile
import shutil
import subprocess
import time

SYNTH_DIR = project_root() / ".windsurf" / "synth"

def relpath(p: Path) -> str:
  try:
  return str(p.relative_to(project_root()).as_posix())
  except Exception:
  return p.as_posix()

def _list_changesets() -> List[Tuple[int, Path]]:
  items: List[Tuple[int, Path]] = []
  for p in SYNTH_DIR.glob("changeset_*.json"):
  try:
  n = int(p.stem.split("_")[-1])
  except Exception:
  continue
  items.append((n, p))
  items.sort(key=lambda t: t[0])
  return items

def read_changeset(idx: Optional[int] = None) -> List[str]:
  items = _list_changesets()
  if not items:
  return []
  if idx is None:
  target = items[-1][1]
  else:
  target = SYNTH_DIR / f"changeset_{idx}.json"
  if not target.exists():
  return []
  with target.open("r", encoding="utf-8") as fh:
  data = json.load(fh)
  return [it.get("path") for it in data.get("files", []) if it.get("path")]

def has_file(*names: str) -> bool:
  root = project_root()
  for n in names:
  if (root / n).exists():
  return True
  return False

def which(cmd: str) -> Optional[str]:
  return shutil.which(cmd)

def validate_python(files: List[str]) -> Tuple[bool, Dict]:
  py_files = [f for f in files if f.endswith(".py")]
  result = {"compiled": 0, "errors": []}
  ok = True
  for f in py_files:
  try:
  py_compile.compile(str(project_root() / f), doraise=True)
  result["compiled"] += 1
  except Exception as e:
  ok = False
  result["errors"].append({"file": f, "error": str(e)})
  # Ruff or pyflakes if available/configured
  lint_tool = None
  lint_errors: List[Dict] = []
  if which("ruff") and (
  has_file("pyproject.toml", ".ruff.toml", "ruff.toml") or True
  ):
  lint_tool = "ruff"
  cmd = ["ruff", "check", *py_files]
  elif which("python3"):
  lint_tool = "pyflakes"
  cmd = ["python3", "-m", "pyflakes", *py_files]
  else:
  cmd = []
  if py_files and cmd:
  proc = subprocess.run(
  cmd, cwd=str(project_root()), capture_output=True, text=True
  )
  if proc.returncode != 0:
  ok = False
  output = (proc.stdout or "") + (proc.stderr or "")
  # Collect last 500 chars to keep output small
  lint_errors.append({"tool": lint_tool, "output_tail": output[-500:]})
  result["lint"] = {"tool": lint_tool or "none", "errors": lint_errors}
  # mypy if configured
  if has_file("mypy.ini", "pyproject.toml") and which("mypy") and py_files:
  proc = subprocess.run(
  ["mypy", "--no-error-summary", *py_files],
  cwd=str(project_root()),
  capture_output=True,
  text=True,
  )
  if proc.returncode != 0:
  ok = False
  result["mypy"] = {
  "errors_tail": ((proc.stdout or "") + (proc.stderr or ""))[-500:]
  }
  else:
  result["mypy"] = {"ok": True}
  return ok, result

def validate_ts_js(files: List[str]) -> Tuple[bool, Dict]:
  ts_files = [f for f in files if f.endswith((".ts", ".tsx"))]
  js_files = [f for f in files if f.endswith((".js", ".jsx"))]
  ok = True
  result: Dict = {"ts": {"checked": len(ts_files)}, "js": {"checked": len(js_files)}}
  if has_file("tsconfig.json") and which("tsc") and ts_files:
  proc = subprocess.run(
  ["tsc", "--noEmit"], cwd=str(project_root()), capture_output=True, text=True
  )
  if proc.returncode != 0:
  ok = False
  result["ts"]["errors_tail"] = ((proc.stdout or "") + (proc.stderr or ""))[
  -500:
  ]
  # eslint if configured
  eslintrc = any(
  has_file(n)
  for n in [
  ".eslintrc.js",
  ".eslintrc.cjs",
  ".eslintrc.json",
  ".eslintrc.yaml",
  ".eslintrc.yml",
  ]
  )
  if eslintrc and which("eslint") and (ts_files or js_files):
  targets = ts_files + js_files
  proc = subprocess.run(
  ["eslint", *targets],
  cwd=str(project_root()),
  capture_output=True,
  text=True,
  )
  if proc.returncode != 0:
  ok = False
  result["eslint"] = {
  "errors_tail": ((proc.stdout or "") + (proc.stderr or ""))[-500:]
  }
  return ok, result

def validate_data(files: List[str]) -> Tuple[bool, Dict]:
  ok = True
  result: Dict = {
  "json": {"checked": 0, "errors": []},
  "yaml": {"checked": 0, "errors": []},
  }
  for f in files:
  p = project_root() / f
  if f.endswith(".json"):
  result["json"]["checked"] += 1
  try:
  txt = p.read_text(encoding="utf-8")
  # Accept empty/whitespace as valid
  if not txt.strip():
  continue
  json.loads(txt)
  except Exception as e:
  ok = False
  result["json"]["errors"].append({"file": f, "error": str(e)})
  elif f.endswith((".yaml", ".yml")):
  result["yaml"]["checked"] += 1
  try:
  import yaml  # type: ignore

  txt = p.read_text(encoding="utf-8")
  if not txt.strip():
  continue
  # Multi-doc support
  docs = list(yaml.safe_load_all(txt))
  _ = docs
  except ModuleNotFoundError:
  # Skip YAML if PyYAML not present
  result["yaml"]["skipped"] = True
  except Exception as e:
  ok = False
  result["yaml"]["errors"].append({"file": f, "error": str(e)})
  return ok, result

def main(argv: Optional[List[str]] = None) -> int:
  argv = argv if argv is not None else sys.argv[1:]
  ap = argparse.ArgumentParser(description="Validate synthesized files")
  ap.add_argument(
  "--changeset",
  type=int,
  default=0,
  help="Validate a specific changeset index. 0=last",
  )
  args = ap.parse_args(argv)

  files = read_changeset(idx=(None if args.changeset == 0 else args.changeset))
  start = time.time()
  report: Dict = {"changed_files": files}

  p_ok, p_res = validate_python(files)
  t_ok, t_res = validate_ts_js(files)
  d_ok, d_res = validate_data(files)

  passed = bool(p_ok and t_ok and d_ok)
  report.update(
  {
  "python": p_res,
  "ts_js": t_res,
  "data": d_res,
  "duration_sec": round(time.time() - start, 3),
  "passed": passed,
  "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
  }
  )
  out = SYNTH_DIR / "validate.json"
  out.parent.mkdir(parents=True, exist_ok=True)
  tmp = out.with_suffix(out.suffix + ".tmp")
  with tmp.open("w", encoding="utf-8") as fh:
  json.dump(report, fh, indent=2)
  fh.write("\n")
  os.replace(tmp, out)
  print(f"[synth] Validation passed={passed}")
  return 0 if passed else 1

if __name__ == "__main__":
  raise SystemExit(main())
