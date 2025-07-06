"""
AIFOLIO SAFE AI Vault Bundle Planner
- Suggests static bundles for admin review
"""


from typing import List, Dict, Any, Set, Tuple

def vault_bundle_planner(vaults: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    """
    SAFE AI-compliant: Static vault bundle planner. Deterministic, owner-controlled, no adaptive logic.
    """
    bundles: List[Dict[str, Any]] = []
    seen: Set[Tuple[str, ...]] = set()
    for v in vaults:
        tag_tuple = tuple(sorted(v["tags"]))
        if tag_tuple not in seen:
            seen.add(tag_tuple)
            bundles.append({"bundle_tags": v["tags"], "vault_ids": [v["vault_id"]]})
        else:
            for b in bundles:
                if set(b["bundle_tags"]) == set(v["tags"]):
                    b["vault_ids"].append(v["vault_id"])
    return {"bundles": bundles}
