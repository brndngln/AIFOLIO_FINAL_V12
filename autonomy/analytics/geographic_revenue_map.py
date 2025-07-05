"""
AIFOLIO SAFE AI Geographic Revenue Map
- Aggregate, static, no geo-targeting
"""


def geographic_revenue_map(sales):
    # Expects: list of {'country': str, 'revenue': int}
    geo = {}
    for s in sales:
        geo[s["country"]] = geo.get(s["country"], 0) + s["revenue"]
    return {"geo_revenue": geo}
