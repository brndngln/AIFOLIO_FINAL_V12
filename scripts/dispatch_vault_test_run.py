import json
from autonomy.pipeline.listeners import vault_test_run

if __name__ == "__main__":
    payload = {
        "run_id": "demo_run",
        "vault_path": "vaults/demo_vault",
        "alert_email_opt_in": False,
    }
    result = vault_test_run.handle_event(payload)
    print(json.dumps(result, indent=2))
