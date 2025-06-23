"""
SAFE AI Static Module: Vault Meta-Market Mapping
- Maps vaults to meta-markets (static, table-driven)
- Logs all mappings for admin review
- No adaptive or emergent behavior
"""
import logging
from datetime import datetime

LOG_PATH = "../../distribution/legal_exports/vault_meta_market_log.txt"
logging.basicConfig(filename=LOG_PATH, level=logging.INFO)

META_MARKET_TABLE = {
    "legal": ["regulatory", "compliance"],
    "finance": ["banking", "investment"],
    "education": ["K-12", "higher ed"]
}

def map_vault_to_meta_market(vault_type, triggered_by):
    timestamp = datetime.utcnow().isoformat()
    meta_markets = META_MARKET_TABLE.get(vault_type, [])
    event = f"[{timestamp}] META-MARKET: {vault_type} -> {meta_markets} | Triggered by: {triggered_by}"
    logging.info(event)
    return meta_markets
