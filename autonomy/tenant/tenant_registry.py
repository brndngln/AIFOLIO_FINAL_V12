"""SAFE AI MODULE"""

ct = None  # TODO: Define ct
config = {}  # TODO: Define config
TENANTS = {}  # TODO: Define TENANTS

"SAFE AI MODULE"
"SAFE AI MODULE"
from typing import Any, Dict


def get_tenant_config(tenant_id: str) -> Dict[str, Any]:
    return TENANTS.get(tenant_id, TENANTS["aifolio"])
