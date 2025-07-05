"""
AIFOLIO SAFE AI Legacy Content Aging Tracker
- Static, aggregate, admin-reviewed
"""


def legacy_content_aging_tracker(contents):
    # Expects: list of {'content_id': str, 'created': 'YYYY-MM-DD'}
    import datetime

    today = datetime.datetime.now().date()
    report = []
    for c in contents:
        created = datetime.datetime.strptime(c["created"], "%Y-%m-%d").date()
        age_years = (today - created).days // 365
        report.append({"content_id": c["content_id"], "age_years": age_years})
    return {"legacy_aging_report": report}
