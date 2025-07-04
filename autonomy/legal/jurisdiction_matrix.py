"""
SAFE AI Jurisdiction Matrix — Phase 10+
Static, Charter-Enforced
"""
from typing import Dict

def get_jurisdiction_matrix() -> Dict[str, Dict[str, str]]:
    """Return static jurisdiction matrix per vault/currency"""
    return {
        "AIFOLIO": {"USD": "US", "EUR": "EU"},
        "REBEL REMEDIES": {"USD": "US"},
        "MINIQUE": {"USD": "US"},
        "QuantumTraderAI": {"USD": "US", "BTC": "Global"},
    }
