"""
AIFOLIO Admin Tools: Log Viewer UI (SAFE AI)
- Allows admin to view/export analytics and pipeline logs
- No automation, no optimization, all manual
"""
def view_log(log_path):
    with open(log_path) as f:
        return f.read()
