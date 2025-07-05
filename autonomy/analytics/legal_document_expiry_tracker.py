"""
AIFOLIO SAFE AI Legal Document Expiry Tracker
- Flags legal docs nearing expiry
"""


def legal_document_expiry_tracker(docs):
    # Expects: list of {'doc_id': str, 'expiry': 'YYYY-MM-DD'}
    import datetime

    today = datetime.datetime.now().date()
    flagged = [
        d
        for d in docs
        if (datetime.datetime.strptime(d["expiry"], "%Y-%m-%d").date() - today).days
        < 30
    ]
    return {"expiring_soon": flagged}
