"""
AIFOLIO SAFE AI Vault Bundle Planner
- Suggests static bundles for admin review
"""
def vault_bundle_planner(vaults):
    # Expects: list of {'vault_id': str, 'tags': list}
    bundles = []
    seen = set()
    for v in vaults:
        tag_tuple = tuple(sorted(v['tags']))
        if tag_tuple not in seen:
            seen.add(tag_tuple)
            bundles.append({'bundle_tags': v['tags'], 'vault_ids': [v['vault_id']]})
        else:
            for b in bundles:
                if set(b['bundle_tags']) == set(v['tags']):
                    b['vault_ids'].append(v['vault_id'])
    return {'bundles': bundles}
