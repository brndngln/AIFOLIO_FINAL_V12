"""
SAFE AI static vault content uniqueness analyzer
- Flags vaults that are too similar to others (static, no cross-vault learning)
- 100% static, non-sentient, suggest-only
"""
def check_content_uniqueness(vault_content, all_vaults):
    # Static comparison: flag if >90% text overlap with any other vault
    flagged = []
    for v in all_vaults:
        if v == vault_content:
            continue
        overlap = len(set(vault_content.split()) & set(v.split())) / max(1, len(set(vault_content.split())))
        if overlap > 0.9:
            flagged.append(v)
    return flagged
