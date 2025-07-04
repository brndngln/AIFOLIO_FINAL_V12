// Style tuner for OMNIELITE: global and per-vault
import globalThemes from '../config/themes/global.json';
import vaultThemes from '../config/themes/vaults.json';

export function getVaultTheme(vaultId, style) {
  const base = globalThemes[style] || globalThemes['elite'];
  const vault = (vaultThemes[vaultId] && vaultThemes[vaultId][style]) ? vaultThemes[vaultId][style] : {};
  return { ...base, ...vault };
}
