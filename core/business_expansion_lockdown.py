# business_expansion_lockdown.py
# No new business/vault/strategy unless unlocked by founder
class BusinessExpansionLockdown:
    def __init__(self, founder_key: str) -> None:
        """
        Initializes the business expansion lockdown with a founder key.
        Args:
            founder_key: The founder's secret key for unlocking expansion.
        """
        self.founder_key: str = founder_key

    def unlock(self, request: str, key: str) -> bool:
        """
        Unlocks business expansion if the correct founder key is provided.
        Args:
            request: The unlock request (not used in logic, but required for interface).
            key: The key provided for unlocking.
        Returns:
            True if the key matches the founder key, False otherwise.
        """
        return key == self.founder_key
