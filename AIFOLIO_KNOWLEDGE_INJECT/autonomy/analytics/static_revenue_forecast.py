"""
AIFOLIO SAFE AI Static Revenue Forecasting (calendar-based only)
- Projects revenue if trends stay constant (no learning, no prediction)
"""


def static_revenue_forecast(revenue_by_month):
    # Expects: {'YYYY-MM': value, ...}
    if not revenue_by_month:
        return {"forecast": 0}
    last_month = list(sorted(revenue_by_month.keys()))[-1]
    forecast = revenue_by_month[last_month]
    return {"next_month_forecast": forecast}
