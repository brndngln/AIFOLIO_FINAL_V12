"""
AIFOLIO SAFE AI Static Competitor Comparison
- Manual input only, compares static aggregate stats
"""


def competitor_comparison(our_stats, competitor_stats):
    # Expects: dicts of aggregate stats
    result = {}
    for k in our_stats:
        result[k] = {"ours": our_stats[k], "competitor": competitor_stats.get(k)}
    return result
