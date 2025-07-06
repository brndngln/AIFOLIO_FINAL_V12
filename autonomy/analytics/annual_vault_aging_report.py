"""
AIFOLIO SAFE AI Annual Vault Aging Report
- Reports vault age in years
"""


from typing import List, Dict, TypedDict

class Vault(TypedDict):
    vault_id: str
    created: str

class AgingReportEntry(TypedDict):
    vault_id: str
    age_years: int

class AgingReport(TypedDict):
    aging_report: List[AgingReportEntry]


def annual_vault_aging_report(vaults: List[Vault]) -> AgingReport:
    # Expects: list of {'vault_id': str, 'created': 'YYYY-MM-DD'}
    import datetime

    today = datetime.datetime.now().date()
    report = []
    for v in vaults:
        created = datetime.datetime.strptime(v["created"], "%Y-%m-%d").date()
        age_years = (today - created).days // 365
        report.append({"vault_id": v["vault_id"], "age_years": age_years})
    return {"aging_report": report}
