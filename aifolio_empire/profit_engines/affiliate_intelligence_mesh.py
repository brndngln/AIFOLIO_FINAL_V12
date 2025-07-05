"""
AIFOLIO™ Affiliate Intelligence Mesh
Identifies influencers, generates links, tracks conversion and tier payouts. SAFE AI: static, deterministic, owner-controlled.
"""
import logging

STATIC_INFLUENCERS = ["@influencer1", "@influencer2"]
STATIC_TIERS = ["Bronze", "Silver", "Gold"]


def get_affiliate_link(user_handle, tier="Bronze"):
    if user_handle not in STATIC_INFLUENCERS:
        return None
    if tier not in STATIC_TIERS:
        tier = "Bronze"
    link = f"https://aifolio.com/aff/{user_handle}/{tier}"
    logging.info(
        f"Affiliate Intelligence Mesh: Handle {user_handle}, Tier: {tier}, Link: {link}"
    )
    return {"handle": user_handle, "tier": tier, "link": link}
