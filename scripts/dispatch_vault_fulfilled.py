import sys
import json
from autonomy.pipeline.listeners import vault_fulfilled

if __name__ == "__main__":
    payload = {
        "vault_id": "demo_vault",
        "buyer_email": "demo@buyer.com",
        "vault_path": "vaults/demo_vault",
        "alert_email_opt_in": True,
        "owner_email": "owner@demo.com"
    }
    result = vault_fulfilled.handle_event(payload)
    print(json.dumps(result, indent=2))
