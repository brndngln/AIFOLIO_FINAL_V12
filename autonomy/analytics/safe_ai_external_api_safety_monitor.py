"""
AIFOLIO SAFE AI External API Safety Monitor
- Static, aggregate, no active adaptation
"""


def external_api_safety_monitor(api_configs):
    # Expects: list of {'api': str, 'compliant': bool}
    flagged = [a for a in api_configs if not a["compliant"]]
    return {"non_compliant_apis": flagged}
