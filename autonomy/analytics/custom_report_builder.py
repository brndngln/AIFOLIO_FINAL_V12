"""
Custom Report Builder for SAFE AI Empire
Static, per-tenant, admin approval required
"""
from typing import Dict, List, Any

def build_custom_report(tenant_id: str, modules: List[str], fields: List[str]) -> Dict[str, Any]:
    """Build a static custom report from selected modules/fields (SAFE AI only)"""
    # Placeholder: returns static sample data
    report = {"tenant": tenant_id, "modules": modules, "fields": fields, "data": []}
    for m in modules:
        report["data"].append({"module": m, "fields": {f: f"sample_{f}" for f in fields}})
    return report
