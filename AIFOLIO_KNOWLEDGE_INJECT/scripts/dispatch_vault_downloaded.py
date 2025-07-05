import json
from autonomy.pipeline.listeners import vault_downloaded

if __name__ == "__main__":
    payload = {
        "vault_id": "demo_vault",
        "user_id": "user_demo",
        "ip": "127.0.0.1",
        "region": "US",
        "vault_path": "vaults/demo_vault",
        "alert_email_opt_in": False,
    }
    result = vault_downloaded.handle_event(payload)
    print(json.dumps(result, indent=2))
