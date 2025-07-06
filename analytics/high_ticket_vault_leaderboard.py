"""
Static, deterministic leaderboard for high-ticket vaults. SAFE AI, owner-controlled, fully auditable.
"""
# High-Ticket Vault Leaderboard
from core.compliance.sentience_firewall import sentience_firewall


from typing import List, Dict, Any
from core.compliance.sentience_firewall import sentience_firewall

@sentience_firewall
def high_ticket_vault_leaderboard(vaults: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Return leaderboard sorted by profitability, engagement, and trend."""
    sorted_vaults = sorted(
        vaults,
        key=lambda v: (v.get("profit", 0), v.get("engagement", 0), v.get("trend", 0)),
        reverse=True,
    )
    return sorted_vaults[:10]
