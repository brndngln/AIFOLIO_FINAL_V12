from fastapi import APIRouter, Query, Request, Body
from fastapi.responses import JSONResponse
from pathlib import Path
import json
from datetime import datetime

from security.mfa_verifier import verify_mfa_token
from security.freeze_controller import get_rotation_enabled, set_rotation_enabled
from security.manual_override_guard import check_manual_override
from security.role_manager import is_admin_in_role

router = APIRouter()
LOG_PATH = Path(__file__).parent.parent.parent / 'logs' / 'secret_rotation.json'
USAGE_PATH = Path(__file__).parent.parent.parent / 'logs' / 'usage_metrics.json'
ANOMALY_PATH = Path(__file__).parent.parent.parent / 'logs' / 'usage_anomalies.json'
OVERRIDE_PATH = Path(__file__).parent.parent.parent / 'logs' / 'override_attempts.json'

@router.get("/api/logs/secret_rotation", response_class=JSONResponse)
def get_secret_rotation_log(
    key: str = Query(None, description="Filter by secret key name"),
    status: str = Query(None, description="Filter by rotation status (SUCCESS/FAIL/VERIFY_FAIL/FALLBACK_LAST_KNOWN)"),
    start: str = Query(None, description="Start date (YYYY-MM-DD)"),
    end: str = Query(None, description="End date (YYYY-MM-DD)")
):
    if not LOG_PATH.exists():
        return []
    with open(LOG_PATH, 'r') as f:
        try:
            logs = json.load(f)
        except Exception:
            logs = []
    # Filtering
    if key:
        logs = [log for log in logs if log.get('key') == key]
    if status:
        logs = [log for log in logs if log.get('status') == status]
    if start:
        logs = [log for log in logs if log.get('timestamp', '')[:10] >= start]
    if end:
        logs = [log for log in logs if log.get('timestamp', '')[:10] <= end]
    return logs

@router.post("/api/rotation/manual_override", response_class=JSONResponse)
def manual_override(request: Request, data: dict = Body(...)):
    from security.alert_hooks import send_slack_alert, send_discord_alert
    admin_id = data.get('adminId')
    token = data.get('code')
    ip = request.client.host
    # RBAC: Only OWNER/OPERATOR can override
    if not (is_admin_in_role(admin_id, 'OWNER') or is_admin_in_role(admin_id, 'OPERATOR')):
        return JSONResponse({"success": False, "error": "Insufficient role for manual override."}, status_code=403)
    allowed, lockout = check_manual_override(admin_id, token, ip)
    if lockout:
        send_slack_alert(f"[AIFOLIO] Manual override lockout for {admin_id} from {ip}")
        send_discord_alert(f"[AIFOLIO] Manual override lockout for {admin_id} from {ip}")
        return JSONResponse({"success": False, "error": "Too many failed attempts. Locked for 15 minutes."}, status_code=403)
    if not allowed:
        return JSONResponse({"success": False, "error": "MFA failed."}, status_code=401)
    # Allow rotation logic here (call rotate_secret.py or similar)
    send_slack_alert(f"[AIFOLIO] Manual override SUCCESS by {admin_id} from {ip}")
    send_discord_alert(f"[AIFOLIO] Manual override SUCCESS by {admin_id} from {ip}")
    return {"success": True}

@router.get("/api/rotation/enabled", response_class=JSONResponse)
def get_rotation_status():
    enabled = get_rotation_enabled()
    # Optionally, get last changed timestamp from Redis or config
    return {"enabled": enabled, "timestamp": datetime.utcnow().isoformat()}

@router.post("/api/rotation/toggle", response_class=JSONResponse)
def toggle_rotation(data: dict = Body(...)):
    from security.alert_hooks import send_slack_alert, send_discord_alert
    admin_id = data.get('adminId')
    code = data.get('code')
    enabled = data.get('enabled')
    # RBAC: Only OWNER can freeze/unfreeze
    if not is_admin_in_role(admin_id, 'OWNER'):
        return JSONResponse({"success": False, "error": "Insufficient role for freeze toggle."}, status_code=403)
    if not verify_mfa_token(admin_id, code):
        return JSONResponse({"success": False, "error": "MFA failed."}, status_code=401)
    set_rotation_enabled(enabled, admin_id)
    action = 'RESUMED' if enabled else 'FROZEN'
    send_slack_alert(f"[AIFOLIO] Rotations {action} by {admin_id}")
    send_discord_alert(f"[AIFOLIO] Rotations {action} by {admin_id}")
    return {"success": True, "enabled": enabled, "timestamp": datetime.utcnow().isoformat()}

@router.get("/api/usage/metrics", response_class=JSONResponse)
def get_usage_metrics():
    if not USAGE_PATH.exists():
        return {}
    with open(USAGE_PATH, 'r') as f:
        return json.load(f)

@router.get("/api/usage/anomalies", response_class=JSONResponse)
def get_usage_anomalies():
    if not ANOMALY_PATH.exists():
        return []
    with open(ANOMALY_PATH, 'r') as f:
        return json.load(f)

@router.post("/api/usage/auto-freeze", response_class=JSONResponse)
def set_auto_freeze(data: dict = Body(...)):
    from security.alert_hooks import send_slack_alert, send_discord_alert
    admin_id = data.get('adminId', 'unknown')
    enable = data.get('enable', False)
    # RBAC: Only OWNER can change auto-freeze
    if not is_admin_in_role(admin_id, 'OWNER'):
        return JSONResponse({"success": False, "error": "Insufficient role for auto-freeze toggle."}, status_code=403)
    config_path = Path(__file__).parent.parent.parent / 'config' / 'vault_control_flags.json'
    if config_path.exists():
        with open(config_path, 'r') as f:
            flags = json.load(f)
    else:
        flags = {}
    flags['auto_freeze_on_spike'] = enable
    flags['last_changed'] = datetime.utcnow().isoformat()
    with open(config_path, 'w') as f:
        json.dump(flags, f, indent=2)
    action = 'ENABLED' if enable else 'DISABLED'
    send_slack_alert(f"[AIFOLIO] Auto-freeze {action} by {admin_id}")
    send_discord_alert(f"[AIFOLIO] Auto-freeze {action} by {admin_id}")
    return {"success": True, "auto_freeze": enable, "timestamp": flags['last_changed']}
