import json
from autonomy.pipeline.listeners import export_failed

if __name__ == "__main__":
    payload = {
        "vault_id": "demo_vault",
        "vault_path": "vaults/demo_vault",
        "alert_email_opt_in": False
    }
    result = export_failed.handle_event(payload)
    print(json.dumps(result, indent=2))
