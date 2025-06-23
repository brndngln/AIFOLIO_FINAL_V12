"""
SAFE AI Static Module: IP Violation Monitor
- Flags potential IP violations using static, table-driven logic
- Logs all scans for admin review
- No adaptive or emergent behavior
"""
import logging
from datetime import datetime

LOG_PATH = "../../distribution/legal_exports/ip_violation_log.txt"
logging.basicConfig(filename=LOG_PATH, level=logging.INFO)

IP_VIOLATION_TABLE = {
    "vault1": False,
    "vault2": True,
    "vault3": False
}

def scan_ip_violation(vault_id, triggered_by):
    timestamp = datetime.utcnow().isoformat()
    violation = IP_VIOLATION_TABLE.get(vault_id, None)
    event = f"[{timestamp}] IP VIOLATION: {vault_id} = {violation} | Triggered by: {triggered_by}"
    logging.info(event)
    return violation
