import json
import datetime
import os

OWNER_LOCK = True
AUDIT_LOG = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../analytics/ai_audit_bot_log.jsonl'))
os.makedirs(os.path.dirname(AUDIT_LOG), exist_ok=True)

# --- AI Audit Bot for Vault Generation Compliance (Static, Rule-Based) ---
def audit_vault(vault):
    issues = []
    if not vault.get('title'):
        issues.append('Missing title')
    if not vault.get('description'):
        issues.append('Missing description')
    if len(vault.get('title', '')) < 5:
        issues.append('Title too short')
    entry = {
        'timestamp': datetime.datetime.utcnow().isoformat() + 'Z',
        'vault': vault,
        'issues': issues
    }
    with open(AUDIT_LOG, 'a') as f:
        f.write(json.dumps(entry) + '\n')
    return issues
