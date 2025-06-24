"""
Static Module Registry for Per-Tenant Customization
"""
from typing import Dict, List

MODULES = {
    "vault": "SAFE AI Vault & Revenue Mesh",
    "analytics": "Analytics & Forecasting Core",
    "compliance": "Compliance & Audit Layer",
    "governance": "Legal & Governance Mesh",
    "marketplace": "SAFE AI PDF Marketplace",
    "arbitrage": "Cross-Market Arbitrage Scanner",
    "optimizer": "Capital Optimizer",
    # Add more modules as needed
}

def get_enabled_modules(tenant_id: str, tenant_registry) -> List[str]:
    config = tenant_registry.get_tenant_config(tenant_id)
    return config.get("enabled_modules", list(MODULES.keys()))
