"""
AIFOLIO Admin Tools: Audit Inspector (SAFE AI)
- Allows admin to inspect all analytics, compliance, and pipeline logs
- No automation, all manual, all actions logged
"""
def inspect_audit(log_paths):
    logs = {}
    for path in log_paths:
        try:
            with open(path) as f:
                logs[path] = f.read()
        except Exception as e:
            logs[path] = str(e)
    return logs
