"""
SAFE AI Static Module: Supply-Demand Imbalance Monitor
- Flags static supply-demand imbalances (table-driven)
- Logs all detections for admin review
- No adaptive or emergent behavior
"""
import logging
from datetime import datetime

LOG_PATH = "../../distribution/legal_exports/supply_demand_imbalance_log.txt"
logging.basicConfig(filename=LOG_PATH, level=logging.INFO)

IMBALANCE_TABLE = {
    "vault1": "balanced",
    "vault2": "oversupply",
    "vault3": "undersupply"
}

def monitor_supply_demand(vault_id, triggered_by):
    timestamp = datetime.utcnow().isoformat()
    imbalance = IMBALANCE_TABLE.get(vault_id, "unknown")
    event = f"[{timestamp}] SUPPLY-DEMAND IMBALANCE: {vault_id} = {imbalance} | Triggered by: {triggered_by}"
    logging.info(event)
    return imbalance
