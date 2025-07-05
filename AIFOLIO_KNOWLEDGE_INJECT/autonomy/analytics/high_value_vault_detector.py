"""
AIFOLIO SAFE AI High-Value Vault Detector
- Flags vaults with revenue above static threshold
"""


def high_value_vault_detector(vaults, threshold=10000):
    return [v for v in vaults if v.get("revenue", 0) >= threshold]
