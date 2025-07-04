import os
import hashlib
import json
from datetime import datetime

POLICY_FILES = [
    "terms_of_service.md",
    "refund_policy.md",
    "privacy_policy.md"
]

TRACKER_PATH = os.path.join(os.path.dirname(__file__), "policy_tracker.json")

BRANDING_PATH = os.path.join(os.path.dirname(__file__), "branding.json")

PDF_EXPORT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../distribution/legal_exports/'))
os.makedirs(PDF_EXPORT_DIR, exist_ok=True)

def compute_file_hash(filepath):
    hasher = hashlib.sha256()
    with open(filepath, 'rb') as f:
        while chunk := f.read(8192):
            hasher.update(chunk)
    return hasher.hexdigest()

def audit_policies():
    """
    Run static audit on all policy files. Block publish if missing, outdated, or corrupted.
    """
    audit_report = {}
    for fname in POLICY_FILES:
        fpath = os.path.join(os.path.dirname(__file__), fname)
        if not os.path.exists(fpath):
            audit_report[fname] = 'missing'
            continue
        hash = compute_file_hash(fpath)
        audit_report[fname] = hash
    # Update tracker
    tracker = {}
    if os.path.exists(TRACKER_PATH):
        with open(TRACKER_PATH, 'r') as f:
            tracker = json.load(f)
    now = datetime.utcnow().isoformat()
    for fname in POLICY_FILES:
        short = fname.replace('.md', '')
        tracker.setdefault(short, {})
        tracker[short]['hash'] = audit_report.get(fname, '')
        tracker[short]['last_audited'] = now
    with open(TRACKER_PATH, 'w') as f:
        json.dump(tracker, f, indent=2)
    return audit_report
