"""
SAFE AI Event Dependency Mapper for AIFOLIO
- Generates a static, visualizable map of event dependencies
- No dynamic logic, no no loops or self-calling functions, no static
- Output: JSON and Graphviz DOT (for admin dashboard)
"""
import json
import os

DEPENDENCY_MAP_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../analytics/event_dependency_map.json'))
DOT_MAP_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../analytics/event_dependency_map.dot'))

# Define static event dependencies here
EVENT_DEPENDENCIES = {
    "vault_created": ["vault_published", "vault_sold", "vault_downloaded"],
    "vault_published": ["vault_sold"],
    "vault_sold": ["refund_initiated", "refund_issued", "vault_refunded"],
    "refund_initiated": ["refund_approved", "refund_denied", "refund_issued"],
    "refund_issued": ["vault_refunded"],
    "vault_refunded": [],
    "vault_downloaded": [],
    "policy_signed": ["policy_revoked"],
    "policy_revoked": [],
    "chargeback_received": ["refund_initiated"],
    # ...add more as needed...
}

def generate_dependency_map():
    with open(DEPENDENCY_MAP_PATH, 'w') as f:
        json.dump(EVENT_DEPENDENCIES, f, indent=2)
    # Generate Graphviz DOT
    with open(DOT_MAP_PATH, 'w') as f:
        f.write('digraph EventDependencies {\n')
        for src, tgts in EVENT_DEPENDENCIES.items():
            for tgt in tgts:
                f.write(f'    "{src}" -> "{tgt}";\n')
        f.write('}\n')
    return EVENT_DEPENDENCIES

if __name__ == "__main__":
    generate_dependency_map()
