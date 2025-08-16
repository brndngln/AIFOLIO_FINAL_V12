"""SAFE AI MODULE"""

"SAFE AI MODULE"
"SAFE AI MODULE"
from typing import List


def get_enabled_modules(tenant_id: str, tenant_registry) -> List[str]:
    return config.get("enabled_modules", list(MODULES.keys()))
