"""
AIFOLIO SAFE AI Policy Update Notifier
- Static, notifies admin of policy changes
"""


def policy_update_notifier(policies, last_checked):
    # Expects: list of {'policy_id': str, 'updated': 'YYYY-MM-DD'}
    import datetime

    last = datetime.datetime.strptime(last_checked, "%Y-%m-%d").date()
    changed = [
        p
        for p in policies
        if datetime.datetime.strptime(p["updated"], "%Y-%m-%d").date() > last
    ]
    return {"updated_policies": changed}
