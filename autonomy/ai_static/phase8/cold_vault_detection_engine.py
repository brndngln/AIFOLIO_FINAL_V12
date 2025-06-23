"""
SAFE AI Static Module: Cold Vault Detection Engine
- Identifies vaults falling out of market demand (table-driven)
- Logs all detections for admin review
- No adaptive or emergent behavior
"""
import logging
from datetime import datetime

LOG_PATH = "../../distribution/legal_exports/cold_vault_detection_log.txt"
logging.basicConfig(filename=LOG_PATH, level=logging.INFO)

COLD_VAULTS = {
    "vault1": False,
    "vault2": True,
    "vault3": False
}

def detect_cold_vault(vault_id, triggered_by):
    timestamp = datetime.utcnow().isoformat()
    is_cold = COLD_VAULTS.get(vault_id, None)
    event = f"[{timestamp}] COLD VAULT: {vault_id} = {is_cold} | Triggered by: {triggered_by}"
    logging.info(event)
    return is_cold
