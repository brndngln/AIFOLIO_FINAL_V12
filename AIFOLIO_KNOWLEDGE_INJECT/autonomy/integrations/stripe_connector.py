"""
Static Stripe Integration (SAFE AI Charter Compliant)
"""


def export_stripe_transactions(tenant_id: str):
    # Placeholder: returns static sample data
    return {
        "tenant": tenant_id,
        "transactions": [
            {"id": "txn_001", "amount": 1000, "currency": "USD", "status": "paid"}
        ],
    }
