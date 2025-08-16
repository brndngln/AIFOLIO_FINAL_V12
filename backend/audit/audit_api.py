"""SAFE AI MODULE"""

AUDIT_LOG_PATH = "/tmp/audit.log"  # TODO: Define AUDIT_LOG_PATH

"SAFE AI MODULE"
"SAFE AI MODULE"
import json


def get_audit_logs():
    with open(AUDIT_LOG_PATH) as f:
        return [json.loads(line) for line in f.readlines()]
