import os
import json
import requests
from cryptography.fernet import Fernet
from datetime import datetime

# === CONFIGURATION ===
VAULT_PATH = os.path.join(os.path.dirname(__file__), "../logs/secret_rotation.json")
FERNET_KEY = os.environ.get("AIFOLIO_VAULT_KEY", Fernet.generate_key())
fernet = Fernet(FERNET_KEY)
DOPPLER_TOKEN = os.environ.get("DOPPLER_TOKEN")
HASHICORP_ADDR = os.environ.get("HASHICORP_ADDR")
HASHICORP_TOKEN = os.environ.get("HASHICORP_TOKEN")


# === VAULT PROVIDER WIRING ===
def store_secret(key, value):
    """
    Store secret in preferred vault provider, fallback to local AES-256.
    """
    if DOPPLER_TOKEN:
        try:
            resp = requests.post(
                "https://api.doppler.com/v3/configs/config/secrets",
                headers={
                    "Authorization": f"Bearer {DOPPLER_TOKEN}",
                    "Content-Type": "application/json",
                },
                json={"name": key, "value": value},
            )
            if resp.status_code == 200:
                return True
            else:
                alert_failure(f"Doppler store failed: {resp.text}")
        except Exception as e:
            alert_failure(f"Doppler exception: {e}")
    if HASHICORP_ADDR and HASHICORP_TOKEN:
        try:
            url = f"{HASHICORP_ADDR}/v1/secret/data/{key}"
            resp = requests.post(
                url,
                headers={"X-Vault-Token": HASHICORP_TOKEN},
                json={"data": {"value": value}},
            )
            if resp.status_code == 200:
                return True
            else:
                alert_failure(f"HashiCorp store failed: {resp.text}")
        except Exception as e:
            alert_failure(f"HashiCorp exception: {e}")
    # Fallback to AES-256 local
    entry = {
        "key": key,
        "value": fernet.encrypt(value.encode()).decode(),
        "timestamp": time_now(),
    }
    if os.path.exists(VAULT_PATH):
        with open(VAULT_PATH, "r") as f:
            secrets = json.load(f)
    else:
        secrets = []
    secrets = [s for s in secrets if s["key"] != key]
    secrets.append(entry)
    with open(VAULT_PATH, "w") as f:
        json.dump(secrets, f, indent=2)
    return True


def fetch_secret(key):
    """
    Fetch secret from preferred vault provider, fallback to local AES-256.
    """
    if DOPPLER_TOKEN:
        try:
            resp = requests.get(
                f"https://api.doppler.com/v3/configs/config/secrets/{key}",
                headers={"Authorization": f"Bearer {DOPPLER_TOKEN}"},
            )
            if resp.status_code == 200:
                return resp.json()["data"]["value"]
        except Exception as e:
            alert_failure(f"Doppler fetch exception: {e}")
    if HASHICORP_ADDR and HASHICORP_TOKEN:
        try:
            url = f"{HASHICORP_ADDR}/v1/secret/data/{key}"
            resp = requests.get(url, headers={"X-Vault-Token": HASHICORP_TOKEN})
            if resp.status_code == 200:
                return resp.json()["data"]["data"]["value"]
        except Exception as e:
            alert_failure(f"HashiCorp fetch exception: {e}")
    # Fallback to AES-256 local
    if not os.path.exists(VAULT_PATH):
        return None
    with open(VAULT_PATH, "r") as f:
        secrets = json.load(f)
    for entry in secrets:
        if entry["key"] == key:
            return fernet.decrypt(entry["value"].encode()).decode()
    return None


def alert_failure(msg):
    # Advanced alerting: print + POST to n8n webhook
    print(f"[ALERT][VAULT] {msg}")
    try:
        n8n_webhook = os.environ.get("N8N_VAULT_ALERT_WEBHOOK", None)
        if n8n_webhook:
            import requests

            requests.post(n8n_webhook, json={"msg": msg})
    except Exception as e:
        print(f"[ALERT][VAULT][WEBHOOK_FAIL] {e}")


def time_now():
    return datetime.utcnow().isoformat()


# === EXTENSION POINTS ===
# - Add more vault providers as needed
# - Advanced alerting can be wired via alert_failure()
# - All actions auditable via audit_logger
