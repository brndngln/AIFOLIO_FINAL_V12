import requests
import os

# --- Tax Provider API Keys (set in environment) ---
TAXJAR_API_KEY = os.getenv("TAXJAR_API_KEY")
AVALARA_API_KEY = os.getenv("AVALARA_API_KEY")
VATLAYER_API_KEY = os.getenv("VATLAYER_API_KEY")

class TaxEngine:
    @staticmethod
    def get_tax_rate(country_code, state_code=None, vat_id=None):
        """
        Returns dict: {tax_rate, region, vat_id_valid}
        Tries TaxJar, then Avalara, then VATLayer (EU only)
        """
        # --- TaxJar Integration ---
        if TAXJAR_API_KEY:
            headers = {"Authorization": f"Bearer {TAXJAR_API_KEY}"}
            params = {"country": country_code}
            if state_code: params["state"] = state_code
            try:
                r = requests.get("https://api.taxjar.com/v2/rates/" + country_code, headers=headers, params=params)
                if r.status_code == 200:
                    data = r.json().get("rate", {})
                    return {
                        "tax_rate": float(data.get("combined_rate", 0)),
                        "region": f"{country_code} - {state_code}" if state_code else country_code,
                        "vat_id_valid": True if vat_id else None
                    }
            except Exception:
                pass
        # --- Avalara (stub) ---
        if AVALARA_API_KEY:
            # In production, call Avalara AvaTax API
            return {
                "tax_rate": 0.08,
                "region": f"{country_code} - {state_code}" if state_code else country_code,
                "vat_id_valid": True if vat_id else None
            }
        # --- VATLayer (EU fallback) ---
        if country_code in ["DE", "FR", "IT", "ES", "NL", "BE", "AT", "SE", "PL", "DK", "FI", "GR", "IE", "PT", "LU", "CZ", "HU", "SK", "SI", "EE", "LV", "LT", "BG", "RO", "HR", "CY", "MT"] and VATLAYER_API_KEY:
            try:
                r = requests.get(f"http://apilayer.net/api/rate?access_key={VATLAYER_API_KEY}&country_code={country_code}")
                if r.status_code == 200:
                    data = r.json()
                    return {
                        "tax_rate": float(data.get("standard_rate", 0)),
                        "region": country_code,
                        "vat_id_valid": data.get("valid", False) if vat_id else None
                    }
            except Exception:
                pass
        # --- Default fallback ---
        return {"tax_rate": 0.0, "region": country_code, "vat_id_valid": False}
