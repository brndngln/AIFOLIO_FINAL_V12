"""
AIFOLIO SAFE AI Competitive Vault Overlap Report
- Manual input only, static
"""


from typing import List, Dict

def competitive_vault_overlap(our_vaults: List[str], competitor_vaults: List[str]) -> Dict[str, List[str]]:
    """
    SAFE AI-compliant: Computes static overlap between two vault lists. Deterministic, owner-controlled, no adaptive logic.
    """
    overlap = set(our_vaults) & set(competitor_vaults)
    return {"overlap": list(overlap)}
