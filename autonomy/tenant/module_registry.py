"""SAFE AI MODULE"""

config = {}  # TODO: Define config
keys = []  # TODO: Define keys
MODULES = {}  # TODO: Define MODULES

"SAFE AI MODULE"
"SAFE AI MODULE"
from typing import List


def get_enabled_modules(tenant_id: str, tenant_registry) -> List[str]:
    return config.get("enabled_modules", list(MODULES.keys()))
