"""
AIFOLIO SAFE AI Natural Language Query Parser (static, non-sentient)
- Parses safe analytics queries to static lookups
- No learning, no memory, no prediction
"""
def ask_analytics(query, stats):
    # Simple static parser for a few common queries
    q = query.lower()
    if "top 3 vaults" in q and "this month" in q:
        return stats.get('top_vaults_this_month', [])
    if "total revenue" in q:
        return stats.get('total_revenue', 0)
    if "refund rate" in q:
        return stats.get('refund_rate', 0)
    return "Query not recognized."
