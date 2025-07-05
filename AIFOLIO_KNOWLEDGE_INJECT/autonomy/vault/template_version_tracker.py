import json
import datetime

# Emma Compliance Lock
OWNER_LOCK = True
import os

TEMPLATE_LOG = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__), "../../analytics/template_version_log.jsonl"
    )
)
os.makedirs(os.path.dirname(TEMPLATE_LOG), exist_ok=True)


# --- Vault Template Version Tracking ---
def track_template_version(vault_id, template_id, version):
    entry = {
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "vault_id": vault_id,
        "template_id": template_id,
        "version": version,
    }
    with open(TEMPLATE_LOG, "a") as f:
        f.write(json.dumps(entry) + "\n")
    return entry
