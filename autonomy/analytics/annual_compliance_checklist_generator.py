"""
AIFOLIO SAFE AI Annual Compliance Checklist Generator
- Static, generates annual compliance items for review
"""
def annual_compliance_checklist(year):
    # Expects: year (int)
    checklist = [
        'Review privacy policy',
        'Confirm receipt delivery compliance',
        'Audit refund/return policy',
        'Check vault legal clause updates',
        'Verify GDPR/CCPA opt-out handling',
        'Review admin audit logs',
        'Update compliance documentation'
    ]
    return {'year': year, 'checklist': checklist}
