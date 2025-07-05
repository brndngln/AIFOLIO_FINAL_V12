"""
AIFOLIO Storefront Analytics (SAFE AI)
- Tracks page views, clicks, conversions (aggregate only)
- Conversion funnel stats, static reporting
- No personal data, no targeting, no optimization
"""


def storefront_analytics(data):
    # Expects: {'page_views': int, 'clicks': int, 'conversions': int}
    funnel = {
        "page_views": data.get("page_views", 0),
        "clicks": data.get("clicks", 0),
        "conversions": data.get("conversions", 0),
        "click_through_rate": (data.get("clicks", 0) / data.get("page_views", 1)) * 100
        if data.get("page_views", 0)
        else 0,
        "conversion_rate": (data.get("conversions", 0) / data.get("clicks", 1)) * 100
        if data.get("clicks", 0)
        else 0,
    }
    return funnel
