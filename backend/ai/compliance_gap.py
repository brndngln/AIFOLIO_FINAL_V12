import json
from pathlib import Path

POLICY_PATH = Path(__file__).parent.parent / "config" / "safe_ai_policies.json"
MAPPING_PATH = Path(__file__).parent.parent / "logs" / "policy_external_mapping.json"
GAP_PATH = Path(__file__).parent.parent / "logs" / "compliance_gaps.json"

EXTERNAL_STANDARDS = ["iso27001", "nist80053"]


def analyze_gaps() -> List[Dict[str, str]]:
    """
    SAFE AI-compliant: Static compliance gap analysis. Deterministic, owner-controlled, no adaptive logic.
    """
    if not MAPPING_PATH.exists():
        return []
    with open(MAPPING_PATH, "r") as f:
        mappings = json.load(f)
    gaps: List[Dict[str, str]] = []
    for std in EXTERNAL_STANDARDS:
        covered: Set[str] = {m["external_mapping"][std] for m in mappings}
        required: Set[str] = set()
        if std == "iso27001":
            required = {"A.9.2.4", "A.9.4.2", "A.12.4.1", "A.18.2.2"}
        elif std == "nist80053":
            required = {"AC-2", "IA-2", "AU-6", "PL-2"}
        missing = required - covered
        for m in missing:
            gaps.append({"standard": std, "control": m, "status": "missing"})
    with open(GAP_PATH, "w") as f:
        json.dump(gaps, f, indent=2)
    return gaps
