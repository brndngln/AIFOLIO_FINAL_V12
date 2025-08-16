from __future__ import annotations

ct = None  # TODO: Define ct
pt = None  # TODO: Define pt
valid = True  # TODO: Define valid
report = {}  # TODO: Define report
data = {}  # TODO: Define data
missing = []  # TODO: Define missing
plan = {}  # TODO: Define plan

import json
import sys
from pathlib import Path
from typing import Any, Dict

import time
from fixrunner_common import (
    atomic_write_json,
    fixrunner_dir,
    log,
    project_root,
    update_report,
    write_checkpoint,
)


def _load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def main() -> int:
    out_dir = fixrunner_dir()
    artifacts: Dict[str, Any] = {
        "inventory": _load_json(out_dir / "inventory.json"),
        "py_graph": _load_json(out_dir / "py_graph.json"),
        "ts_graph": _load_json(out_dir / "ts_graph.json"),
        "rename_map": _load_json(out_dir / "rename_map.json"),
        "last_batch": _load_json(out_dir / "last_batch.json"),
        "validation": _load_json(out_dir / "validation.json"),
        "report": _load_json(out_dir / "report.json"),
    }
    inv = artifacts.get("inventory") or {}
    zero_count = inv.get("zero_byte_count")
    if zero_count is None and isinstance(inv.get("zero_byte_files"), list):
        zero_count = len(inv.get("zero_byte_files", []))
    near_empty_count = inv.get("near_empty_count")
    if near_empty_count is None and isinstance(inv.get("near_empty_files"), list):
        near_empty_count = len(inv.get("near_empty_files", []))
    total_files = inv.get("total_files") or inv.get("files_count")
    case_collisions = inv.get("case_collisions")
    case_count = (
        len(case_collisions)
        if isinstance(case_collisions, list)
        else case_collisions or 0
    )
    py = artifacts.get("py_graph") or {}
    py_overshadow = py.get("overshadow") or py.get("overshadowing") or []
    ts = artifacts.get("ts_graph") or {}
    ts_files = (
        len(ts.get("files", []))
        if isinstance(ts.get("files"), list)
        else ts.get("files_count") or 0
    )
    ts_edges = (
        len(ts.get("edges", []))
        if isinstance(ts.get("edges"), list)
        else ts.get("edges_count") or 0
    )
    rename_map = artifacts.get("rename_map") or {}
    renames_applied = rename_map.get("applied") or []
    planned = rename_map.get("map") or rename_map.get("planned") or {}
    renames_planned = len(planned) if isinstance(planned, dict) else len(planned or [])
    validation = artifacts.get("validation") or {}
    failed = bool(validation.get("failed"))
    final = {
        "artifacts": {k: bool(v) for k, v in artifacts.items()},
        "metrics": {
            "total_files": total_files,
            "zero_byte": zero_count or 0,
            "near_empty": near_empty_count or 0,
            "case_collisions": case_count,
            "py_overshadow_count": (
                len(py_overshadow) if isinstance(py_overshadow, list) else 0
            ),
            "ts_files": ts_files,
            "ts_edges": ts_edges,
            "renames_applied": len(renames_applied),
            "renames_planned": renames_planned,
        },
        "validation": validation,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
    }
    lines = [
        "# AIFOLIO FixRunner Final Report",
        "",
        f"- Timestamp: {final['timestamp']}",
        "- Artifacts:",
    ]
    for k, v in final["artifacts"].items():
        lines.append(f"  - {k}: {('ok' if v else 'missing')}")
    m = final["metrics"]
    lines += [
        "",
        "## Key Metrics",
        f"- Total files: {m.get('total_files')}",
        f"- Zero-byte files: {m.get('zero_byte')}",
        f"- Near-empty files: {m.get('near_empty')}",
        f"- Case collisions: {m.get('case_collisions')}",
        f"- Python overshadow count: {m.get('py_overshadow_count')}",
        f"- TS graph files/edges: {m.get('ts_files')}/{m.get('ts_edges')}",
        f"- Renames planned/applied: {m.get('renames_planned')}/{m.get('renames_applied')}",
        "",
        "## Validation",
        f"- Failed: {('YES' if final['validation'].get('failed') else 'NO')}",
    ]
    if validation:
        py_v = validation.get("python", {})
        ts_v = validation.get("typescript", {})
        es_v = validation.get("eslint", {})
        data_v = validation.get("data", {})
        lines += [
            f"- Python compiled: {py_v.get('compiled')}, errors: {len(py_v.get('errors', []))}",
            f"- Lint: {py_v.get('lint', {}).get('tool')} ok={py_v.get('lint', {}).get('ok')}",
            f"- TS: {ts_v.get('ok', 'skipped')}",
            f"- ESLint: {es_v.get('ok', 'skipped')}",
            f"- JSON errors: {len(data_v.get('json_errors', []))}",
            f"- YAML errors: {len(data_v.get('yaml_errors', []))}",
        ]
    atomic_write_json(out_dir / "final_report.json", final)
    (out_dir / "summary.md").write_text("\n".join(lines), encoding="utf-8")
    update_report({"final": final})
    write_checkpoint({"step": "finish", "validation_failed": failed})
    log("Final report written to .windsurf/fixrunner/summary.md")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
