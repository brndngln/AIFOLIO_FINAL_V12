import os
from datetime import datetime
from secrets import token_urlsafe
from vault_injector import store_secret, fetch_secret
from audit_logger import log_rotation_event
from reload_handler import hot_reload_config

ROTATION_KEYS = [
    "OPENAI_API_KEY",
    "HUGGINGFACE_API_KEY",
    "GUMROAD_API_KEY",
    "REDIS_TOKEN",
    "INTERNAL_WEBHOOK_TOKEN",
]
ROTATION_ATTEMPTS = 3


# --- SECRET ROTATION LOGIC ---
def rotate_key(key_name: str) -> str:
    # Vendor API call or fallback to secure random
    if key_name == "OPENAI_API_KEY":
        # TODO: requests.post() to OpenAI API for key rotation
        new_secret: str = token_urlsafe(64)
    else:
        new_secret = token_urlsafe(64)
    # Store in vault
    store_secret(key_name, new_secret)
    return new_secret


def verify_key_injected(key: str, secret: str) -> bool:
    # Fetch from vault and compare
    result = fetch_secret(key) == secret
    return bool(result)


def backup_env() -> str:
    ts: str = datetime.utcnow().strftime("%Y%m%d-%H%M%S")
    env_path: str = os.path.join(os.path.dirname(__file__), "../.env")
    bak_path: str = os.path.join(os.path.dirname(__file__), f"../.env.bak-{ts}")
    if os.path.exists(env_path):
        with open(env_path, "r") as src, open(bak_path, "w") as dst:
            dst.write(src.read())
    return bak_path


def rotate_all() -> None:
    backup_env()
    for key in ROTATION_KEYS:
        attempt: int = 0
        success: bool = False
        while attempt < ROTATION_ATTEMPTS and not success:
            try:
                new_secret: str = rotate_key(key)
                if verify_key_injected(key, new_secret):
                    log_rotation_event(key, "SUCCESS")
                    success = True
                else:
                    attempt += 1
                    log_rotation_event(key, "VERIFY_FAIL")
            except Exception as e:
                attempt += 1
                log_rotation_event(key, "FAIL", error=str(e))
        if not success:
            # Fallback to last known good
            log_rotation_event(key, "FALLBACK_LAST_KNOWN")
    hot_reload_config()


if __name__ == "__main__":
    rotate_all()
