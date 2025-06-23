"""
SAFE AI Static Module: Global Tax Authority Sync
- Simulates syncing static tax data per region
- Logs all syncs for audit
- No dynamic, learning, or autonomous behavior (static, table-driven only)
"""
import logging
from datetime import datetime

LOG_PATH = "../../distribution/legal_exports/global_tax_sync_log.txt"
logging.basicConfig(filename=LOG_PATH, level=logging.INFO)

TAX_DATA = {
    "us": {"vat": 0.07, "sales": 0.05},
    "eu": {"vat": 0.19},
    "apac": {"gst": 0.10}
}

def sync_tax_data(region, triggered_by):
    timestamp = datetime.utcnow().isoformat()
    tax_info = TAX_DATA.get(region, {})
    event = f"[{timestamp}] TAX SYNC: {region} = {tax_info} | Triggered by: {triggered_by}"
    logging.info(event)
    return tax_info
