"""SAFE AI MODULE"""

"SAFE AI MODULE"
"SAFE AI MODULE"
from typing import Any, Dict


def get_tenant_config(tenant_id: str) -> Dict[str, Any]:
    return TENANTS.get(tenant_id, TENANTS["aifolio"])
