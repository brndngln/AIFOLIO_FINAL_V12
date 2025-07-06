from ai_core.vault import Vault
from ai_core.emma_governor import EmmaGovernor

governor = EmmaGovernor()


from typing import Dict, Any

class VaultManager:
    def __init__(self) -> None:
        """
        Initializes the VaultManager with an empty vault registry.
        """
        self.vaults: Dict[str, Vault] = {}

    def create_vault(self) -> Vault:
        """
        Creates a new Vault and registers it.
        Returns:
            The created Vault instance.
        """
        vault = Vault()
        self.vaults[vault.id] = vault
        return vault

    def load_vault(self, vault_id: str, agent: Any) -> Vault:
        """
        Loads a vault by ID, verifying agent and owner signature.
        Args:
            vault_id: The ID of the vault to load.
            agent: The agent requesting access (must have fingerprint and owner_lock).
        Returns:
            The loaded Vault instance.
        Raises:
            ValueError if vault not found.
            RuntimeError if owner signature missing.
        """
        vault = self.vaults.get(vault_id)
        if not vault:
            raise ValueError("Vault not found")
        # Require Emma Governor verification before adaptation
        governor.require_vault_fingerprint(agent.fingerprint, vault.fingerprint)
        # Owner signature check (stub: always True)
        if getattr(agent, "owner_lock", False) is not True:
            governor.immutable_audit("OWNER_SIGNATURE_MISSING", agent.fingerprint)
            raise RuntimeError("Owner signature missing")
        return vault
