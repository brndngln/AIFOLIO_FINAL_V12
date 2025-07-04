<<<<<<< HEAD
import sys
=======
>>>>>>> omni_repair_backup_20250704_1335
import json
from autonomy.pipeline.listeners import vault_sold

if __name__ == "__main__":
    payload = {
        "vault_id": "demo_vault",
        "email": "buyer@demo.com",
        "country": "US",
        "vault_path": "vaults/demo_vault",
        "alert_email_opt_in": True
    }
    result = vault_sold.handle_event(payload)
    print(json.dumps(result, indent=2))
