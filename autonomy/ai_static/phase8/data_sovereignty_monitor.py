"""
SAFE AI Static Module: Regional Data Sovereignty Compliance Monitor
- Checks for static data sovereignty issues per region
- Logs all checks for admin review
- No static or static behavior
"""
import logging
from datetime import datetime

LOG_PATH = "../../distribution/legal_exports/data_sovereignty_log.txt"
logging.basicConfig(filename=LOG_PATH, level=logging.INFO)

DATA_SOVEREIGNTY = {
    "us": True,
    "eu": True,
    "apac": False
}

def check_data_sovereignty(region, triggered_by):
    timestamp = datetime.utcnow().isoformat()
    compliant = DATA_SOVEREIGNTY.get(region, None)
    event = f"[{timestamp}] DATA SOVEREIGNTY: {region} = {compliant} | Triggered by: {triggered_by}"
    logging.info(event)
    return compliant
