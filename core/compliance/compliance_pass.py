"""
COMPLIANCE_PASS: Static SAFE AI enforcement utility.
Blocks any high-risk vault/product launch or export unless both legal_review and ethical_compliance_check pass.
"""
def enforce_compliance_pass(compliance_report: dict):
    if not compliance_report.get('legal_review_passed') or not compliance_report.get('ethical_compliance_check_passed'):
        raise Exception("COMPLIANCE_PASS required: legal_review and ethical_compliance_check must pass before launch/export.")
    return True
