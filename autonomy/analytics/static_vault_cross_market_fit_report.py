"""
AIFOLIO SAFE AI Vault Cross-Market Fit Report
- Static, aggregate, admin-reviewed
"""


def vault_cross_market_fit_report(vaults):
    # Expects: list of {'vault_id': str, 'markets': list}
    report = []
    for v in vaults:
        report.append(
            {
                "vault_id": v["vault_id"],
                "markets": v["markets"],
                "cross_market_fit": len(v["markets"]) > 1,
            }
        )
    return {"cross_market_fit": report}
