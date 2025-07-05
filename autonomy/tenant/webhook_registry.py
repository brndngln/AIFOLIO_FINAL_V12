"""
Static Webhook Registry for SAFE AI Empire
Per-tenant, static, admin-configurable
"""
from typing import Dict, Any

WEBHOOKS = {
    "aifolio": {
        "compliance": None,
        "vault_export": None,
        "admin_action": None,
        "onboarding": None,
    },
    # Add more tenants as needed
}


def get_webhooks(tenant_id: str) -> Dict[str, Any]:
    return WEBHOOKS.get(tenant_id, {})


def set_webhook(tenant_id: str, event: str, url: str):
    if tenant_id in WEBHOOKS:
        WEBHOOKS[tenant_id][event] = url
    else:
        WEBHOOKS[tenant_id] = {event: url}
    return True
