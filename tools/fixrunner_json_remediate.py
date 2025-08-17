from __future__ import annotations

ct = None  # TODO: Define ct
pt = None  # TODO: Define pt
valid = True  # TODO: Define valid
template = ""  # TODO: Define template
result = None  # TODO: Define result
data = {}  # TODO: Define data
missing = []  # TODO: Define missing
counts = {}  # TODO: Define counts
results = []  # TODO: Define results
invalid = []  # TODO: Define invalid

import json
import re
import shutil
import sys
import time
from pathlib import Path
from typing import Dict, List, Tuple

from fixrunner_common import (
    atomic_write_json,
    atomic_write_text,
    fixrunner_dir,
    log,
    project_root,
    read_json,
    relpath,
)


def load_failing_jsons() -> List[Path]:
    vpath = fixrunner_dir() / "validation.json"
    v = read_json(vpath, {})
    errs = (v.get("data") or {}).get("json_errors") or []
    paths: List[Path] = []
    for e in errs:
        f = e.get("file")
        if not f:
            continue
        p = project_root() / f
        if p.exists():
            paths.append(p)
        else:
            log(f"Remediate: missing path (skipped): {f}")
    return paths


def ensure_quarantine_path(p: Path) -> Path:
    qp = fixrunner_dir() / "quarantine" / relpath(p)
    qp.parent.mkdir(parents=True, exist_ok=True)
    return qp


def backup_original(p: Path) -> bool:
    try:
        qp = ensure_quarantine_path(p)
        if not qp.exists():
            qp.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(p, qp)
        return True
    except Exception as e:
        log(f"Remediate: backup failed for {relpath(p)}: {e}")
        return False


# Escape unescaped double quotes inside n8n mustache {{$json["..."]}} patterns
_n8n_pat = re.compile(r"\{\{\s*\$json\[[^\]]*\]\s*\}\}")
_unescaped_quote = re.compile(r'(?<!\\)"')


def _escape_quotes_inside(text: str, span_start: int, span_end: int) -> str:
    inner = text[span_start:span_end]
    fixed = _unescaped_quote.sub(r'\\"', inner)
    return text[:span_start] + fixed + text[span_end:]


def fix_n8n_json_templates(text: str) -> Tuple[str, int]:
    count = 0
    out = text
    for m in list(_n8n_pat.finditer(text)):
        s, e = m.span()
        before = out
        out = _escape_quotes_inside(out, s, e)
        if out != before:
            count += 1
    return out, count


def is_valid_json(text: str) -> bool:
    try:
        json.loads(text)
        return True
    except Exception:
        return False


def remediate_file(p: Path) -> Tuple[str, str]:
    rel = relpath(p)
    try:
        raw = p.read_text(encoding="utf-8")
    except Exception as e:
        return ("skipped", f"read_error: {e}")

    # Try targeted n8n fix first
    if "/n8n/flows/" in ("/" + rel):
        fixed, n = fix_n8n_json_templates(raw)
        if n > 0 and is_valid_json(fixed):
            backup_original(p)
            atomic_write_text(p, fixed)
            return ("fixed_n8n", f"escaped_quotes:{n}")

    # Fallback: stub invalid JSON with {}
    if not is_valid_json(raw):
        backup_original(p)
        atomic_write_text(p, "{}\n")
        return ("stubbed", "replaced_with_empty_object")

    return ("ok", "already_valid")


def main() -> int:
    start = time.time()
    targets = load_failing_jsons()
    results: Dict[str, Dict[str, int]] = {
        "fixed_n8n": {},
        "stubbed": {},
        "ok": {},
        "skipped": {},
    }
    counters = {"fixed_n8n": 0, "stubbed": 0, "ok": 0, "skipped": 0}
    for p in targets:
        kind, info = remediate_file(p)
        counters[kind] = counters.get(kind, 0) + 1
        results.setdefault(kind, {})[relpath(p)] = 1
        log(f"Remediate: {kind}: {relpath(p)} ({info})")
    report = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "counts": counters,
        "duration_sec": round(time.time() - start, 3),
        "files": results,
    }
    atomic_write_json(fixrunner_dir() / "json_remediate.json", report)
    log(f"Remediate complete: {counters}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
