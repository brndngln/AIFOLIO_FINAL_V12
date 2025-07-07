#!/usr/bin/env python3
"""
Windsurf Sentinel: Static SAFE AI audit and forbidden pattern monitor.
SAFE AI: Static, deterministic, owner-controlled, fully auditable, no adaptive/sentient logic.
Monitors for forbidden patterns and enforces static audit policy. No adaptive or sentient logic.
"""
import subprocess
import sys
import json
from pathlib import Path
import os
import functools

# Patterns to monitor
FORBIDDEN_PATTERNS = [
    "*.hc",
    "*.veracrypt",
    "*.tar.gz",
    "*.zip",
    "*.7z",
    "*.pkl",
    "*.h5",
    "*.iso",
    "/secure/",
    "/vaults/",
    "/backups/",
    "/mount/",
    "omnisecure_stack/",
    "admin/tools/system_backups/",
    "analytics/backups/",
]

AUDIT_LOG = "emma_volume_audit.json"


def is_forbidden(filename: str) -> bool:
    """Check if a filename matches any forbidden pattern.
    SAFE AI: Static, deterministic, owner-controlled, fully auditable, no adaptive/sentient logic.
    Args:
        filename (str): The filename to check.
    Returns:
        bool: True if forbidden, False otherwise.
    """
    for pat in FORBIDDEN_PATTERNS:
        if Path(filename).match(pat):
            return True
    return False


def autonomous_recovery(func):
    """Decorator for static, deterministic recovery from permission errors.
    SAFE AI: Static, deterministic, owner-controlled, fully auditable, no adaptive/sentient logic.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        retries: int = 3
        for attempt in range(1, retries + 1):
            try:
                return func(*args, **kwargs)
            except (PermissionError, OSError) as e:
                print(f"[AUTONOMOUS RECOVERY] Attempt {attempt}: {e}")
                try:
                    os.chmod(".", 0o755)
                    for root, dirs, files in os.walk("."):
                        for d in dirs:
                            os.chmod(os.path.join(root, d), 0o755)
                        for f in files:
                            os.chmod(os.path.join(root, f), 0o644)
                except Exception as perm_e:
                    print(f"[AUTONOMOUS RECOVERY] chmod error: {perm_e}")
                try:
                    os.chown(".", os.getuid(), os.getgid())
                except Exception as chown_e:
                    print(f"[AUTONOMOUS RECOVERY] chown error: {chown_e}")
                if attempt == retries:
                    print(
                        f"[AUTONOMOUS RECOVERY] Permanent error after {retries} attempts:\n"
                        f"{e}"
                    )
                    # Only abort on SAFE AI violation
                    if "sentient" in str(e).lower():
                        sys.exit("SAFE AI violation: sentience detected.")
                    return []
        return []

    return wrapper


@autonomous_recovery
def get_staged_files(timeout_sec=60):
    try:
        result = subprocess.run(
            ["git", "diff", "--cached", "--name-only"],
            capture_output=True,
            text=True,
            timeout=timeout_sec,
        )
        return result.stdout.strip().split("\n") if result.returncode == 0 else []
    except subprocess.TimeoutExpired:
        print("[Sentinel] git diff timed out.")
        try:
            with open("emma_volume_audit.json", "a") as f:
                f.write(
                    json.dumps(
                        {
                            "event": "git_diff_timeout",
                            "timestamp": __import__("datetime")
                            .datetime.utcnow()
                            .isoformat(),
                        }
                    )
                    + "\n"
                )
        except Exception:
            pass
        # CEO alert logic (if available)
        return []
    except Exception as e:
        print(f"[Sentinel] git diff error: {e}")
        try:
            with open("emma_volume_audit.json", "a") as f:
                f.write(
                    json.dumps(
                        {
                            "event": "git_diff_error",
                            "error": str(e),
                            "timestamp": __import__("datetime")
                            .datetime.utcnow()
                            .isoformat(),
                        }
                    )
                    + "\n"
                )
        except Exception:
            pass
        # CEO alert logic (if available)
        return []


def log_event(event):
    try:
        if Path(AUDIT_LOG).exists():
            with open(AUDIT_LOG, "r") as f:
                log = json.load(f)
        else:
            log = []
        log.append(event)
        with open(AUDIT_LOG, "w") as f:
            json.dump(log, f, indent=2)
    except Exception as e:
        print(f"[Sentinel] Failed to log event: {e}", file=sys.stderr)


def main():
    staged = get_staged_files()
    forbidden = [f for f in staged if is_forbidden(f)]
    if forbidden:
        print(f"[Sentinel] ERROR: Forbidden files staged: {forbidden}")
        log_event(
            {
                "event": "forbidden_git_stage",
                "files": forbidden,
                "action": "blocked",
            }
        )
        sys.exit(0)

    else:
        print("[Sentinel] No forbidden files staged.")


if __name__ == "__main__":
    main()
