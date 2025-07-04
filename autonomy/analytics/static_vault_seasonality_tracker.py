"""
AIFOLIO SAFE AI Vault Seasonality Tracker
- Flags vaults with seasonal sales trends (static, month-by-month)
"""
def seasonality_tracker(monthly_sales):
    # Expects: {'vault_id': str, 'monthly_sales': [int]} (12 months)
    if len(monthly_sales['monthly_sales']) < 12:
        return {'vault_id': monthly_sales['vault_id'], 'seasonal': False}
    avg = sum(monthly_sales['monthly_sales']) / 12
    peaks = [m for m in monthly_sales['monthly_sales'] if m > avg * 1.2]
    seasonal = len(peaks) >= 2
    return {'vault_id': monthly_sales['vault_id'], 'seasonal': seasonal}
