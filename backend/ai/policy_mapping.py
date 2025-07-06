import json
from pathlib import Path
from typing import Dict, List, Any

POLICY_PATH: Path = Path(__file__).parent.parent / "config" / "safe_ai_policies.json"
MAPPING_PATH: Path = Path(__file__).parent.parent / "logs" / "policy_external_mapping.json"

# Static, deterministic, SAFE AI-compliant mapping to external standards
EXTERNAL_STANDARDS: Dict[str, Dict[str, str]] = {
    "iso27001": {
        "rotation": "A.9.2.4 (Management of secret authentication information)",
        "override": "A.9.4.2 (Secure log-on procedures)",
        "anomaly": "A.12.4.1 (Event logging)",
        "workflow": "A.18.2.2 (Compliance with security policies and standards)",
    },
    "nist80053": {
        "rotation": "AC-2 (Account Management)",
        "override": "IA-2 (Identification and Authentication)",
        "anomaly": "AU-6 (Audit Review, Analysis, and Reporting)",
        "workflow": "PL-2 (System and Communications Protection Policy)",
    },
}


def map_policies_to_standards():
    if not POLICY_PATH.exists():
        return []
    with open(POLICY_PATH, "r") as f:
        policies = json.load(f)
    mappings = []
    for p in policies:
        mapped = {}
        for std, stdmap in EXTERNAL_STANDARDS.items():
            mapped[std] = stdmap.get(p["type"], "N/A")
        mappings.append({"policy": p, "external_mapping": mapped})
    with open(MAPPING_PATH, "w") as f:
        json.dump(mappings, f, indent=2)
    return mappings
