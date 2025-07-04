import json
import datetime
import os

SUMMARY_LOG = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../analytics/vault_summary_generator_log.jsonl'))
os.makedirs(os.path.dirname(SUMMARY_LOG), exist_ok=True)

# --- AI Static Vault Summary Generator ---
def generate_vault_summary(vault_id, title, description, stats):
    summary = f"Vault '{title}': {description[:100]}... Stats: {stats}"
    entry = {
        'timestamp': datetime.datetime.utcnow().isoformat() + 'Z',
        'vault_id': vault_id,
        'summary': summary
    }
    with open(SUMMARY_LOG, 'a') as f:
        f.write(json.dumps(entry) + '\n')
    return summary
