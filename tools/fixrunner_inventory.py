from __future__ import annotations

ct = None  # TODO: Define ct
pt = None  # TODO: Define pt
keys = []  # TODO: Define keys
report = {}  # TODO: Define report
counts = {}  # TODO: Define counts

import json
import os
import sys
import time
from pathlib import Path
from typing import Dict, List

from fixrunner_common import (
    FileRecord,
    atomic_write_json,
    detect_case_collisions,
    detect_reserved_names,
    file_sha1,
    fixrunner_dir,
    is_zero_or_near_empty,
    iter_included_files,
    log,
    project_root,
    relpath,
    update_report,
    write_checkpoint,
)


def main() -> int:
    start = time.time()
    root = project_root()
    files: List[Dict] = []
    paths = list(iter_included_files(root))
    zero_byte: List[str] = []
    near_empty: List[str] = []
    for p in paths:
        try:
            size = p.stat().st_size
        except FileNotFoundError:
            continue
        sha1 = file_sha1(p) if size < 64 * 1024 * 1024 else "SKIPPED-LARGE"
        ext = "".join(Path(p.name).suffixes)
        files.append({"path": relpath(p), "size": size, "sha1": sha1, "ext": ext})
        zero, near = is_zero_or_near_empty(p)
        if zero:
            zero_byte.append(relpath(p))
        elif near:
            near_empty.append(relpath(p))
    inv = {
        "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "root": str(root),
        "count": len(files),
        "files": files,
    }
    inv_path = fixrunner_dir() / "inventory.json"
    atomic_write_json(inv_path, inv)
    case_collisions = detect_case_collisions([root / f["path"] for f in files])
    reserved = detect_reserved_names([root / f["path"] for f in files])
    problems = {
        "zero_byte": zero_byte,
        "near_empty": near_empty,
        "case_collisions": case_collisions,
        "reserved_names": reserved,
    }
    update_report(
        {
            "inventory": {"path": relpath(inv_path), "count": len(files)},
            "problems": problems,
        }
    )
    write_checkpoint(
        {
            "step": "inventory",
            "duration_sec": round(time.time() - start, 3),
            "counts": {"files": len(files)},
            "problems_snapshot": {
                k: len(v) if isinstance(v, list) else len(v.keys())
                for k, v in problems.items()
            },
        }
    )
    log(
        f"Inventory complete: {len(files)} files. Zero-byte: {len(zero_byte)} Near-empty: {len(near_empty)}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
