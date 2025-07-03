// OMNIELITE Vault Manager: Loads, registers, and dynamically loads vaults
import vaultRegistry from '../config/vault_registry.json';

export function getVaultList() {
  return vaultRegistry;
}

export function loadVault(vaultId) {
  // Dynamically import vault UI/component logic
  return import(`../vaults/${vaultId}/logic.js`);
}
