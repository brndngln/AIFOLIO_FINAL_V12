"""
AIFOLIO SAFE AI Vault Lifecycle Stage Tracker
- Flags vaults by static lifecycle stage (e.g., launch, mature, sunset)
"""


def vault_lifecycle_stage(vaults):
    # Expects: list of {'vault_id': str, 'created': 'YYYY-MM-DD', 'last_sale': 'YYYY-MM-DD'}
    import datetime

    today = datetime.datetime.now().date()
    result = {}
    for v in vaults:
        created = datetime.datetime.strptime(v["created"], "%Y-%m-%d").date()
        last_sale = (
            datetime.datetime.strptime(v["last_sale"], "%Y-%m-%d").date()
            if v.get("last_sale")
            else created
        )
        age_days = (today - created).days
        since_last_sale = (today - last_sale).days
        if age_days < 90:
            stage = "launch"
        elif since_last_sale > 180:
            stage = "sunset"
        else:
            stage = "mature"
        result[v["vault_id"]] = stage
    return result
