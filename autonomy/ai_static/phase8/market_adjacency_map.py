"""
SAFE AI Static Module: Market Adjacency Map
- Maps new industries/niches adjacent to current markets (static, table-driven)
- Logs all map generations for admin review
- No static or static behavior
"""
import logging
from datetime import datetime

LOG_PATH = "../../distribution/legal_exports/market_adjacency_map_log.txt"
logging.basicConfig(filename=LOG_PATH, level=logging.INFO)

ADJACENCY_TABLE = {
    "legal": ["compliance", "risk management"],
    "finance": ["insurance", "fintech"],
    "education": ["edtech", "corporate training"],
}


def generate_market_adjacency(current_market, triggered_by):
    timestamp = datetime.utcnow().isoformat()
    adjacents = ADJACENCY_TABLE.get(current_market, [])
    event = f"[{timestamp}] MARKET ADJACENCY: {current_market} -> {adjacents} | Triggered by: {triggered_by}"
    logging.info(event)
    return adjacents
