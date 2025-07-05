"""
SAFE AI Static Module: Cashflow Projection Engine
- Projects cashflow using static, preconfigured values
- Logs all projections for admin review
- No dynamic, learning, or autonomous behavior (static, table-driven only)
"""
import logging
from datetime import datetime

LOG_PATH = "../../distribution/legal_exports/cashflow_projection_log.txt"
logging.basicConfig(filename=LOG_PATH, level=logging.INFO)

CASHFLOW_PROJECTIONS = {"January": 5000, "February": 5200, "March": 4800}


def project_cashflow(triggered_by):
    timestamp = datetime.utcnow().isoformat()
    event = f"[{timestamp}] CASHFLOW PROJECTION: {CASHFLOW_PROJECTIONS} | Triggered by: {triggered_by}"
    logging.info(event)
    return CASHFLOW_PROJECTIONS
