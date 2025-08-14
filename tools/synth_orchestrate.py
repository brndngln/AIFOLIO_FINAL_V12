#!/usr/bin/env python3
"""
Synth Orchestrator

Runs the full AIFOLIO synthesis pipeline end-to-end in atomic batches:
- synth_apply per batch (default size=20)
- synth_validate per resulting changeset
- AST-aware import/reference fixes (TS/JS then Python): dry-run, apply if needed, re-validate
- Commit each changeset atomically using its manifest with --no-verify
- Periodically refresh summary

Safety and guarantees:
- Never touches project-root __init__.py (enforced by tools/synth_fix_imports.py logic)
- Atomic per-changeset commits; no mixed changes across commits
- Stops on validation errors and reports context
- Produces structured logs under .windsurf/synth/orchestrate/

Usage examples:
  python3 tools/synth_orchestrate.py --resume
  python3 tools/synth_orchestrate.py --start-batch 66 --end-batch 120 --size 20 --summary-every 25
"""
from __future__ import annotations

import argparse
import math
import json
import os
import re
import shlex
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional, Tuple

REPO_ROOT = Path(__file__).resolve().parents[1]
TOOLS_DIR = REPO_ROOT / "tools"
SYNTH_DIR = REPO_ROOT / ".windsurf" / "synth"
LOG_DIR = SYNTH_DIR / "orchestrate"
LOG_DIR.mkdir(parents=True, exist_ok=True)
RUN_LOG = LOG_DIR / "run.log"


@dataclass
class CmdResult:
    rc: int
    out: str
    err: str


def run(cmd: str, cwd: Path | None = None, check: bool = False) -> CmdResult:
    p = subprocess.run(
        cmd,
        cwd=cwd or REPO_ROOT,
        shell=True,
        text=True,
        capture_output=True,
    )
    if check and p.returncode != 0:
        raise RuntimeError(f"Command failed rc={p.returncode}: {cmd}\nSTDOUT\n{p.stdout}\nSTDERR\n{p.stderr}")
    return CmdResult(p.returncode, p.stdout, p.stderr)


def log_event(event: str, **fields):
    rec = {"ts": datetime.now(timezone.utc).isoformat(), "event": event, **fields}
    RUN_LOG.parent.mkdir(parents=True, exist_ok=True)
    with RUN_LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps(rec, sort_keys=True) + "\n")


CHGSET_RE = re.compile(r"changeset\s+(\d+)")


def parse_changeset_from_apply_output(out: str) -> Optional[int]:
    # Expect line like: "[synth] Wrote 20 files into changeset 64"
    for line in out.splitlines():
        m = CHGSET_RE.search(line)
        if m:
            try:
                return int(m.group(1))
            except Exception:
                pass
    return None


def last_committed_changeset_from_git() -> Optional[int]:
    cmd = 'git log --grep "^synth: commit changeset " -n 1 --pretty=format:%s'
    res = run(cmd)
    if res.rc != 0:
        return None
    m = CHGSET_RE.search(res.out)
    if not m:
        return None
    try:
        return int(m.group(1))
    except Exception:
        return None


def validate_changeset(n: int) -> bool:
    res = run(f"python3 tools/synth_validate.py --changeset {n}")
    ok = "Validation passed=True" in res.out
    log_event("validate", changeset=n, rc=res.rc, ok=ok)
    return ok


def fix_imports(changeset: int, kinds: list[str]) -> Tuple[int, bool]:
    planned_total = 0
    applied_any = False
    for group in kinds:
        dry = run(f"python3 tools/synth_fix_imports.py --changesets {changeset} --limit 50 --only {group}")
        planned = 0
        try:
            # first JSON block is on stdout
            j = json.loads(dry.out.splitlines()[0]) if dry.out.strip().startswith("{") else {}
            planned = int(j.get("planned_patches", 0))
        except Exception:
            planned = 0
        log_event("fix_imports_dry", changeset=changeset, group=group, planned=planned, rc=dry.rc)
        planned_total += planned
        if planned > 0:
            ap = run(f"python3 tools/synth_fix_imports.py --changesets {changeset} --limit 50 --only {group} --apply")
            applied_any = True or applied_any
            log_event("fix_imports_apply", changeset=changeset, group=group, rc=ap.rc)
    return planned_total, applied_any


def commit_changeset(n: int) -> bool:
    manifest = SYNTH_DIR / f"changeset_{n}.json"
    if not manifest.exists():
        log_event("commit_skip", changeset=n, reason="manifest_missing")
        return False
    try:
        data = json.loads(manifest.read_text(encoding="utf-8"))
    except Exception as e:
        log_event("commit_skip", changeset=n, reason=f"manifest_read_error: {e}")
        return False
    files = [e.get("path") for e in data.get("files", []) if e.get("path")]
    if not files:
        log_event("commit_skip", changeset=n, reason="no_files")
        return False
    # stage and commit
    run("git reset")
    add_cmd = "git add -- " + " ".join(shlex.quote(p) for p in files)
    add_res = run(add_cmd)
    if add_res.rc != 0:
        log_event("commit_fail", changeset=n, step="git_add", rc=add_res.rc, out=add_res.out, err=add_res.err)
        return False
    staged = run("git diff --cached --name-only")
    if not any(ln.strip() for ln in staged.out.splitlines()):
        log_event("commit_skip", changeset=n, reason="no_staged")
        return False
    ts = data.get("timestamp")
    ts_str = ""
    try:
        if ts is not None:
            ts_str = datetime.fromtimestamp(float(ts), tz=timezone.utc).isoformat()
    except Exception:
        pass
    lines = [
        f"synth: commit changeset {n} ({len(files)} files)",
        "validation: passed; import-fix dry-runs applied as needed",
        f"manifest: .windsurf/synth/changeset_{n}.json",
    ]
    if ts_str:
        lines.append(f"manifest_timestamp_utc: {ts_str}")
    msg = "\n\n".join(lines)
    c = run(f"git commit --no-verify -m {shlex.quote(msg)}")
    ok = c.rc == 0
    log_event("commit", changeset=n, rc=c.rc)
    return ok


def refresh_summary() -> bool:
    res = run("python3 tools/synth_finish.py")
    if res.rc != 0:
        log_event("summary_fail", rc=res.rc, out=res.out, err=res.err)
        return False
    res2 = run("git add .windsurf/synth/summary.md && git commit --no-verify -m 'synth: refresh summary' ")
    log_event("summary_commit", rc=res2.rc)
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--start-batch", type=int, default=None, help="First batch id to apply")
    ap.add_argument("--end-batch", type=int, default=None, help="Inclusive last batch id to apply. If omitted, run until exhaustion.")
    ap.add_argument("--size", type=int, default=20, help="Batch size for synth_apply")
    ap.add_argument("--summary-every", type=int, default=25, help="Refresh summary every N changesets")
    ap.add_argument("--resume", action="store_true", help="Infer start-batch from last committed changeset")
    ap.add_argument("--max-failures", type=int, default=1, help="Abort after this many failures")
    args = ap.parse_args()

    # Determine maximum batch index from candidates, if available
    max_batch: Optional[int] = None
    try:
        cand = json.loads((SYNTH_DIR / "candidates.json").read_text(encoding="utf-8"))
        total_candidates = len(cand.get("candidates") or [])
        if total_candidates:
            max_batch = math.ceil(total_candidates / args.size)
    except Exception:
        max_batch = None

    # Determine start batch
    start_batch: Optional[int] = args.start_batch
    if start_batch is None and args.resume:
        last_cs = last_committed_changeset_from_git()
        if last_cs is not None:
            # Empirically: batch_id == changeset_id + 1
            start_batch = last_cs + 2  # continue with next batch after the last one processed
    if start_batch is None:
        start_batch = 1

    failures = 0
    total_committed = 0
    batch = start_batch

    log_event("orchestrate_start", start_batch=start_batch, end_batch=args.end_batch, size=args.size, max_batch=max_batch)

    while True:
        if args.end_batch is not None and batch > args.end_batch:
            log_event("orchestrate_stop", reason="end_batch_reached", last_batch=batch - 1)
            break
        if max_batch is not None and batch > max_batch:
            log_event("orchestrate_stop", reason="all_batches_exhausted", last_batch=batch - 1, max_batch=max_batch)
            break
        # Apply
        apply_cmd = f"python3 tools/synth_apply.py --batch {batch} --size {args.size}"
        apply_res = run(apply_cmd)
        log_event("apply", batch=batch, rc=apply_res.rc, out=apply_res.out.splitlines()[-1:] or [])
        if apply_res.rc != 0:
            failures += 1
            if failures >= args.max_failures:
                log_event("orchestrate_stop", reason="apply_failed", batch=batch)
                break
            batch += 1
            continue
        cs = parse_changeset_from_apply_output(apply_res.out)
        if cs is None:
            # Empty batch or unexpected output
            out_l = apply_res.out.lower()
            if "nothing to write in this batch" in out_l or "wrote 0 files" in out_l:
                log_event("apply_empty_batch", batch=batch)
                batch += 1
                continue
            if "no candidates" in out_l:
                log_event("orchestrate_stop", reason="no_more_candidates", batch=batch)
                break
            # Treat as failure to avoid loops
            failures += 1
            log_event("apply_parse_fail", batch=batch)
            if failures >= args.max_failures:
                log_event("orchestrate_stop", reason="apply_parse_failed", batch=batch)
                break
            batch += 1
            continue
        # Validate
        if not validate_changeset(cs):
            failures += 1
            log_event("orchestrate_stop", reason="validation_failed", changeset=cs)
            break
        # Import fixes: TS/JS then Python
        planned_tsjs, applied_tsjs = fix_imports(cs, ["ts js"])  # run combined ts/js group
        planned_py, applied_py = fix_imports(cs, ["py"])        # then python group
        if applied_tsjs or applied_py:
            # re-validate after applying fixes
            if not validate_changeset(cs):
                failures += 1
                log_event("orchestrate_stop", reason="post_fix_validation_failed", changeset=cs)
                break
        # Commit
        if not commit_changeset(cs):
            failures += 1
            if failures >= args.max_failures:
                log_event("orchestrate_stop", reason="commit_failed", changeset=cs)
                break
        else:
            total_committed += 1
        # Periodic summary
        if total_committed % args.summary_every == 0:
            refresh_summary()
        # Next
        batch += 1

    # Final summary refresh
    refresh_summary()
    log_event("orchestrate_done", total_committed=total_committed)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        log_event("orchestrate_interrupt")
        sys.exit(130)
    except Exception as e:
        log_event("orchestrate_crash", error=str(e))
        print(f"[orchestrate] fatal: {e}", file=sys.stderr)
        sys.exit(1)
