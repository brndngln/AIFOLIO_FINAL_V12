"""
AIFOLIO SAFE AI Static Vault Re-Promotion Calendar
- Suggests static dates for re-promotion
"""


def vault_repromotion_calendar(vaults):
    # Expects: list of {'vault_id': str, 'last_promo': 'YYYY-MM-DD'}
    import datetime

    today = datetime.datetime.now().date()
    calendar = []
    for v in vaults:
        last_promo = datetime.datetime.strptime(v["last_promo"], "%Y-%m-%d").date()
        if (today - last_promo).days > 180:
            calendar.append(
                {"vault_id": v["vault_id"], "suggested_repromo": str(today)}
            )
    return {"repromotion_calendar": calendar}
