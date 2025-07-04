// Globalization Layer: Clones and localizes vaults for other markets
export class GlobalizationLayer {
  localizeVault(vault, locale, currency) {
    // Stub: Localize vault for a specific market
    const clone = JSON.parse(JSON.stringify(vault));
    clone.locale = locale;
    clone.currency = currency;
    clone.label = `${vault.label} (${locale})`;
    return clone;
  }
  massLocalize(vaults, locales, currencies) {
    let clones = [];
    for(const vault of vaults) {
      for(let i = 0; i < locales.length; i++) {
        clones.push(this.localizeVault(vault, locales[i], currencies[i] || 'USD'));
      }
    }
    return clones;
  }
}
export default new GlobalizationLayer();
