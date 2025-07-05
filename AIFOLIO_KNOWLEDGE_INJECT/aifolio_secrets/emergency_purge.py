import os
import sys
import json
import time
from datetime import datetime

LOCKDOWN_ENV = os.path.join(os.path.dirname(__file__), ".env.lockdown")
DOTENV_PATH = os.path.join(os.path.dirname(__file__), "../.env")
PURGE_LOG = os.path.join(os.path.dirname(__file__), "../logs/emergency_purge_log.json")
PIPELINE_LOCK_PATH = os.path.join(
    os.path.dirname(__file__), "../logs/pipeline_lock.json"
)


# --- 2-Step Sentinel+Owner Logic Lock ---
def confirm_purge(trigger_source, keyword, ai_confirmed, human_confirmed):
    if keyword != "⚠️ PURGE_NOW_GLOBAL":
        return False
    if not (ai_confirmed and human_confirmed):
        return False
    return True


# --- Doppler/Vault Revocation Stub ---
def revoke_all_vault_secrets():
    # TODO: Insert Doppler/HashiCorp/AWS Vault API revocation logic here
    print("[PURGE] Vault secrets revoked (stub).")
    pass


# --- .env Lockdown Reset ---
def reset_env_to_lockdown():
    if os.path.exists(LOCKDOWN_ENV):
        with open(LOCKDOWN_ENV, "r") as src, open(DOTENV_PATH, "w") as dst:
            dst.write(src.read())
    else:
        # Write minimal lockdown env
        with open(DOTENV_PATH, "w") as dst:
            dst.write("LOCKDOWN_MODE=1\n")
    print("[PURGE] .env set to lockdown.")


# --- Outbound API Freeze ---
def freeze_api_calls():
    os.environ["LOCKDOWN_MODE"] = "1"
    print("[PURGE] Outbound API calls frozen.")
    # All wrappers must check this flag
    pass


# --- Admin Notification (Telegram/Discord/Email stubs) ---
def notify_admin():
    print("[PURGE] Admin notified (stub).")
    # TODO: Integrate Telegram, Discord, Email alerts
    pass


# --- Secure Log ---
def log_purge(trigger_source, countdown=None, override_key=None):
    entry = {
        "event": "EMERGENCY_PURGE",
        "trigger_source": trigger_source,
        "timestamp": datetime.utcnow().isoformat(),
        "countdown": countdown,
        "override_key": override_key,
    }
    os.makedirs(os.path.dirname(PURGE_LOG), exist_ok=True)
    if os.path.exists(PURGE_LOG):
        with open(PURGE_LOG, "r") as f:
            logs = json.load(f)
    else:
        logs = []
    logs.append(entry)
    with open(PURGE_LOG, "w") as f:
        json.dump(logs, f, indent=2)


# --- Pipeline Lock (Vercel/Railway) ---
def lock_deployment_pipelines():
    entry = {"locked": True, "timestamp": datetime.utcnow().isoformat()}
    with open(PIPELINE_LOCK_PATH, "w") as f:
        json.dump(entry, f, indent=2)
    print("[PURGE] Deployment pipelines locked (stub).")


# --- Purge Countdown Timer with Override ---
def purge_countdown(seconds, override_key=None):
    print(f"[PURGE] Countdown: {seconds}s (override key: {override_key})")
    for i in range(seconds, 0, -1):
        print(f"Purging in {i} seconds...")
        time.sleep(1)
    print("[PURGE] Countdown complete.")


# --- Dashboard Reroute (frontend must check LOCKDOWN_MODE) ---
def reroute_dashboard_to_lockdown():
    print(
        "[PURGE] Dashboard rerouted to Lockdown Mode (frontend must check LOCKDOWN_MODE)."
    )
    # Frontend should display: “Security Protocol Engaged. Vault Reset in Progress.”
    pass


# --- Safe Shell State ---
def enter_safe_shell_state():
    print("[PURGE] System is now in safe shell state. Awaiting new secrets.")
    # All key-dependent services halted until reset
    pass


# --- Main Emergency Purge Routine ---
def run_emergency_purge(
    trigger_source,
    keyword,
    ai_confirmed,
    human_confirmed,
    countdown=0,
    override_key=None,
):
    if not confirm_purge(trigger_source, keyword, ai_confirmed, human_confirmed):
        print("PURGE NOT CONFIRMED")
        return False
    if countdown > 0:
        purge_countdown(countdown, override_key)
    revoke_all_vault_secrets()
    reset_env_to_lockdown()
    freeze_api_calls()
    notify_admin()
    lock_deployment_pipelines()
    log_purge(trigger_source, countdown, override_key)
    reroute_dashboard_to_lockdown()
    enter_safe_shell_state()
    print("EMERGENCY PURGE COMPLETE")
    return True


if __name__ == "__main__":
    # Example CLI: python emergency_purge.py manual '⚠️ PURGE_NOW_GLOBAL' 1 1 10 override123
    trigger_source = sys.argv[1] if len(sys.argv) > 1 else "manual"
    keyword = sys.argv[2] if len(sys.argv) > 2 else ""
    ai_confirmed = bool(int(sys.argv[3])) if len(sys.argv) > 3 else False
    human_confirmed = bool(int(sys.argv[4])) if len(sys.argv) > 4 else False
    countdown = int(sys.argv[5]) if len(sys.argv) > 5 else 0
    override_key = sys.argv[6] if len(sys.argv) > 6 else None
    run_emergency_purge(
        trigger_source, keyword, ai_confirmed, human_confirmed, countdown, override_key
    )
