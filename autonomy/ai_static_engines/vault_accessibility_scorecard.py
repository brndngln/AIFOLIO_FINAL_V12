"""
SAFE AI static vault accessibility scorecard
- Rates accessibility features (alt text, structure, contrast) with static rules
- 100% static, non-sentient, suggest-only
"""
def score_accessibility(vault_metadata):
    score = 0
    if vault_metadata.get("has_alt_text"): score += 1
    if vault_metadata.get("has_structured_headings"): score += 1
    if vault_metadata.get("contrast_checked"): score += 1
    return score
