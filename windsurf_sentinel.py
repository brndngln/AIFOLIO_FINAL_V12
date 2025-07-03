#!/usr/bin/env python3
import subprocess
import sys
import json
from pathlib import Path

# Patterns to monitor
FORBIDDEN_PATTERNS = [
    '*.hc', '*.veracrypt', '*.tar.gz', '*.zip', '*.7z', '*.pkl', '*.h5', '*.iso',
    '/secure/', '/vaults/', '/backups/', '/mount/',
    'omnisecure_stack/', 'admin/tools/system_backups/', 'analytics/backups/'
]

AUDIT_LOG = 'emma_volume_audit.json'

def is_forbidden(filename):
    for pat in FORBIDDEN_PATTERNS:
        if Path(filename).match(pat):
            return True
    return False

def get_staged_files(timeout_sec=60):
    try:
        result = subprocess.run(['git', 'diff', '--cached', '--name-only'], capture_output=True, text=True, timeout=timeout_sec)
        return result.stdout.strip().split('\n') if result.returncode == 0 else []
    except subprocess.TimeoutExpired:
        print('[Sentinel] git diff timed out.')
        try:
            with open('emma_volume_audit.json', 'a') as f:
                f.write(json.dumps({'event': 'git_diff_timeout', 'timestamp': __import__('datetime').datetime.utcnow().isoformat()}) + '\n')
        except Exception:
            pass
        # CEO alert logic (if available)
        return []
    except Exception as e:
        print(f'[Sentinel] git diff error: {e}')
        try:
            with open('emma_volume_audit.json', 'a') as f:
                f.write(json.dumps({'event': 'git_diff_error', 'error': str(e), 'timestamp': __import__('datetime').datetime.utcnow().isoformat()}) + '\n')
        except Exception:
            pass
        # CEO alert logic (if available)
        return []

def log_event(event):
    try:
        if Path(AUDIT_LOG).exists():
            with open(AUDIT_LOG, 'r') as f:
                log = json.load(f)
        else:
            log = []
        log.append(event)
        with open(AUDIT_LOG, 'w') as f:
            json.dump(log, f, indent=2)
    except Exception as e:
        print(f"[Sentinel] Failed to log event: {e}", file=sys.stderr)

def main():
    staged = get_staged_files()
    forbidden = [f for f in staged if is_forbidden(f)]
    if forbidden:
        print(f"[Sentinel] ERROR: Forbidden files staged: {forbidden}")
        log_event({
            'event': 'forbidden_git_stage',
            'files': forbidden,
            'action': 'blocked',
        })
        sys.exit(1)
    else:
        print("[Sentinel] No forbidden files staged.")

if __name__ == "__main__":
    main()
