// OMNIELITE AIFOLIO i18n/l10n Scaffold
import { createContext } from "react";

export const SupportedLanguages = ["en", "es", "fr", "de", "zh"];
export const I18nContext = createContext({
  lang: "en",
  setLang: () => {},
  t: (key) => key, // fallback: identity
});

// Example usage: <I18nContext.Provider value={{lang, setLang, t}}>
