"""
SAFE AI Static Module: Archive Optimization Bot
- Suggests when vaults should be archived (table-driven)
- Logs all suggestions for admin review
- No adaptive or emergent behavior
"""
import logging
from datetime import datetime

LOG_PATH = "../../distribution/legal_exports/archive_optimization_log.txt"
logging.basicConfig(filename=LOG_PATH, level=logging.INFO)

ARCHIVE_SUGGESTIONS = {
    "vault1": False,
    "vault2": True,
    "vault3": False
}

def suggest_archive(vault_id, triggered_by):
    timestamp = datetime.utcnow().isoformat()
    should_archive = ARCHIVE_SUGGESTIONS.get(vault_id, None)
    event = f"[{timestamp}] ARCHIVE OPTIMIZATION: {vault_id} = {should_archive} | Triggered by: {triggered_by}"
    logging.info(event)
    return should_archive
