"""
AIFOLIO SAFE AI Sales Heatmap by Day/Time
- Aggregate, static, no targeting
"""


def sales_heatmap_by_daytime(sales):
    # Expects: list of {'datetime': 'YYYY-MM-DD HH:MM'}
    import datetime

    heatmap = {}
    for s in sales:
        dt = datetime.datetime.strptime(s["datetime"], "%Y-%m-%d %H:%M")
        key = (dt.strftime("%A"), dt.hour)
        heatmap[key] = heatmap.get(key, 0) + 1
    return {"heatmap": heatmap}
