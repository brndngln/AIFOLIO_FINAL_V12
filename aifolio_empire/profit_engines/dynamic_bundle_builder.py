"""
Dynamic Bundle Builder with strict anti-sentience measures.
This engine simulates creating themed vault bundles with tiered pricing and scarcity.
It is stateless, rule-based, and does not learn or adapt.
"""

import random
import logging
import json
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta

# Attempt to import config and logger
try:
    from config import config, logger
except ImportError:
    print("Warning: Could not import 'config' and 'logger' directly. Using basic logging.")
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    class MockConfig:
        PATTERN_AWARE_ENABLED = False
    config = MockConfig()

# Anti-sentience: Operational parameters for simulation
MAX_VAULTS_PER_BUNDLE = 5
MIN_VAULTS_FOR_BUNDLING = 2
SIMULATED_DISCOUNT_RATES = [0.1, 0.15, 0.2, 0.25, 0.3] # 10% to 30%

class DynamicBundleBuilder:
    """Creates dynamic vault bundles with anti-sentience safeguards."""

    def __init__(self):
        """Initialize the engine. All operations are stateless."""
        self._random_seed = random.randint(1, 1000000) # For internal randomization
        logger.info("DynamicBundleBuilder initialized. Operations are stateless.")

    def simulate_theme_detection(self, vault_title: str, vault_niche: str) -> dict:
        """SAFE AI-compliant: Detects themes from vault title/niche using static rules. Returns dict with result, explanation, recommendation, priority, version, SAFE AI/owner/non-sentient metadata, and audit log."""
        VERSION = "AIFOLIO_DYNAMIC_BUNDLE_BUILDER_V2_SAFEAI_FINAL"
        SAFE_AI_COMPLIANT = True
        OWNER_CONTROLLED = True
        NON_SENTIENT = True
        themes = []
        common_keywords = {
            "Health": ["health", "fitness", "wellness", "diet", "workout"],
            "Business": ["business", "marketing", "finance", "startup", "entrepreneur"],
            "Tech": ["tech", "software", "ai", "crypto", "coding"],
            "Creative": ["creative", "art", "writing", "design", "music"],
            "Lifestyle": ["lifestyle", "self-help", "productivity", "relationships"]
        }
        text_to_scan = f"{vault_title.lower()} {vault_niche.lower()}"
        for theme, keywords in common_keywords.items():
            if any(keyword in text_to_scan for keyword in keywords):
                themes.append(theme)
        if not themes:
            themes.append("General")
        explanation = f"Themes detected: {themes}."
        recommendation = None
        priority = 1
        self._log_action('simulate_theme_detection', {'themes': themes}, explanation, recommendation, priority, VERSION)
        return {
            'result': list(set(themes)),
            'explanation': explanation,
            'recommendation': recommendation,
            'priority': priority,
            'version': VERSION,
            'SAFE_AI_COMPLIANT': SAFE_AI_COMPLIANT,
            'OWNER_CONTROLLED': OWNER_CONTROLLED,
            'NON_SENTIENT': NON_SENTIENT
        }

    def _group_vaults_by_theme(self, available_vaults: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """Groups vaults by simulated themes. Anti-sentience: Grouping is naive and randomized."""
        themed_vaults: Dict[str, List[Dict[str, Any]]] = {}
        for vault in available_vaults:
            # Anti-sentience: Simulate potential failure in theme detection for a vault
            if random.random() < 0.02: # 2% chance to skip a vault for grouping
                logger.warning(f"Simulated failure to categorize vault: {vault.get('title', 'Unknown Vault')}")
                continue

            themes = self._simulate_theme_detection(vault.get('title', ''), vault.get('niche', ''))
            for theme in themes:
                if theme not in themed_vaults:
                    themed_vaults[theme] = []
                themed_vaults[theme].append(vault)
        
        # Anti-sentience: Randomly merge or split theme groups if too many/few
        if len(themed_vaults) > 5 and random.random() < 0.2:
            keys = list(themed_vaults.keys())
            k1, k2 = random.sample(keys, 2)
            themed_vaults[k1].extend(themed_vaults.pop(k2, []))
            logger.warning(f"Simulated random merge of theme groups: {k2} into {k1}")
        
        return themed_vaults

    def _create_bundle_offers(self, theme: str, vaults_in_theme: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Simulates creating bundle offers for a given theme with tiered pricing."""
        bundles = []
        if len(vaults_in_theme) < MIN_VAULTS_FOR_BUNDLING:
            return [] # Not enough vaults for a bundle

        # Shuffle for variety in bundle composition (Anti-sentience)
        random.shuffle(vaults_in_theme)

        # Simulate different bundle types
        # 1. Starter Pack (e.g., 2-3 vaults)
        if len(vaults_in_theme) >= 2:
            num_in_starter = random.randint(2, min(3, len(vaults_in_theme), MAX_VAULTS_PER_BUNDLE))
            starter_vaults = vaults_in_theme[:num_in_starter]
            original_price = sum(v.get('price', 5.0) for v in starter_vaults) # Default price 5 if missing
            discount = random.choice(SIMULATED_DISCOUNT_RATES)
            bundle_price = round(original_price * (1 - discount), 2)
            bundles.append({
                "bundle_name": f"{theme} Starter Pack ({num_in_starter} Vaults)",
                "type": "StarterPack",
                "vault_titles": [v.get('title', 'Untitled Vault') for v in starter_vaults],
                "original_total_price_simulated": original_price,
                "bundle_price_simulated": bundle_price,
                "discount_applied_simulated": f"{discount*100:.0f}%"
            })

        # 2. "Buy X Get Y Free" or "Booster" (e.g., 3-5 vaults)
        if len(vaults_in_theme) >= 3:
            num_in_booster = random.randint(3, min(len(vaults_in_theme), MAX_VAULTS_PER_BUNDLE))
            booster_vaults = vaults_in_theme[:num_in_booster]
            original_price = sum(v.get('price', 5.0) for v in booster_vaults)
            # Simulate a "Buy X Get 1 Free" type discount by making it slightly more aggressive
            discount = random.choice(SIMULATED_DISCOUNT_RATES) + random.uniform(0.05, 0.1) 
            discount = min(discount, 0.4) # Cap discount
            bundle_price = round(original_price * (1 - discount), 2)
            bundles.append({
                "bundle_name": f"{theme} Booster Bundle ({num_in_booster} Vaults)",
                "type": "BoosterPack",
                "vault_titles": [v.get('title', 'Untitled Vault') for v in booster_vaults],
                "original_total_price_simulated": original_price,
                "bundle_price_simulated": bundle_price,
                "discount_applied_simulated": f"{discount*100:.0f}% (Value Deal!)"
            })
        
        # Anti-sentience: Randomly fail to create a bundle type or alter its price nonsensically
        if random.random() < 0.05 and bundles: # 5% chance to mess with a bundle
            idx_to_mess = random.randrange(len(bundles))
            if random.random() < 0.5:
                bundles[idx_to_mess]['bundle_price_simulated'] = round(random.uniform(1.0, 500.0), 2) # Nonsense price
                logger.warning(f"Simulated price corruption for bundle: {bundles[idx_to_mess]['bundle_name']}")
            else:
                bundles.pop(idx_to_mess)
                logger.warning(f"Simulated omission of a bundle for theme {theme}.")

        return bundles

    def _add_scarcity_logic(self, bundle_offer: Dict[str, Any]) -> Dict[str, Any]:
        """Simulates adding scarcity logic to a bundle offer. Rule-based and random."""
        if random.random() < 0.7: # 70% chance to add some scarcity
            scarcity_type = random.choice(["countdown", "bonus_unlock", "limited_stock_simulated"])
            
            if scarcity_type == "countdown":
                sim_hours = random.randint(1, 72)
                bundle_offer["scarcity_simulated"] = f"Offer ends in (simulated) {sim_hours} hours!"
                bundle_offer["simulated_expiry_timestamp"] = (datetime.utcnow() + timedelta(hours=sim_hours)).isoformat()
            elif scarcity_type == "bonus_unlock":
                bonus = random.choice(["Extra Checklist PDF", "Private Q&A Invite (Simulated)", "Early Access to Next Vault"])
                bundle_offer["scarcity_simulated"] = f"Buy now and unlock bonus: {bonus}! (Simulated)"
            else: # limited_stock_simulated
                stock = random.randint(5, 50)
                bundle_offer["scarcity_simulated"] = f"Only {stock} bundles left at this price! (Simulated)"
        
        # Anti-sentience: Scarcity message might be generic or slightly off
        if random.random() < 0.03 and "scarcity_simulated" in bundle_offer:
            bundle_offer["scarcity_simulated"] = "Special offer, check details! (Generic simulated message)"
            logger.warning(f"Simulated generic scarcity message for bundle: {bundle_offer.get('bundle_name')}")

        return bundle_offer

    def generate_dynamic_bundles(self, available_vaults: List[Dict[str, Any]]) -> Optional[List[Dict[str, Any]]]:
        """
        Generates dynamic bundle offers from a list of available vaults.
        Stateless operation with anti-sentience measures.

        Args:
            available_vaults: List of vault data (dicts with 'title', 'niche', 'price').

        Returns:
            A list of generated bundle offers, or None on simulated critical failure.
        """
        # Anti-sentience: Random chance for the entire operation to 'fail'
        if random.random() < 0.01 or not available_vaults: # 1% chance or no vaults
            logger.error("Simulated critical random failure or no vaults provided in generate_dynamic_bundles.")
            return None

        logger.info(f"Generating dynamic bundles from {len(available_vaults)} available vaults.")

        # 1. Group vaults by theme (simulated)
        themed_vault_groups = self._group_vaults_by_theme(available_vaults)
        if not themed_vault_groups:
            logger.warning("No thematic groups could be formed (simulated outcome).")
            return [] # Return empty list if no groups

        all_bundles = []
        for theme, vaults_in_theme in themed_vault_groups.items():
            # Anti-sentience: Randomly skip a theme for bundling
            if random.random() < 0.03:
                logger.warning(f"Simulated random skip of theme for bundling: {theme}")
                continue
            
            theme_bundles = self._create_bundle_offers(theme, vaults_in_theme)
            for bundle in theme_bundles:
                bundle_with_scarcity = self._add_scarcity_logic(bundle)
                all_bundles.append(bundle_with_scarcity)
        
        # Anti-sentience: Shuffle final bundle order
        random.shuffle(all_bundles)

        # Anti-sentience: Randomly omit a successfully generated bundle from the final list
        if all_bundles and random.random() < 0.02:
            omitted_bundle = all_bundles.pop(random.randrange(len(all_bundles)))
            logger.warning(f"Simulated random omission of a final bundle: {omitted_bundle.get('bundle_name')}")

        logger.info(f"Successfully generated {len(all_bundles)} dynamic bundle offers (simulated).")
        return all_bundles

# Example Usage
if __name__ == "__main__":
    logger.info("--- Running DynamicBundleBuilder Example ---")
    bundle_builder = DynamicBundleBuilder()

    # Simulate some available vaults
    sim_vaults_data = [
        {"id": "v001", "title": "AI Content Creation Secrets", "niche": "AI Marketing", "price": 19.99},
        {"id": "v002", "title": "Fitness Over 40 Guide", "niche": "Health & Wellness", "price": 14.50},
        {"id": "v003", "title": "Beginner's Guide to Crypto", "niche": "Tech Finance", "price": 24.99},
        {"id": "v004", "title": "Advanced SEO Strategies", "niche": "Business Marketing", "price": 29.99},
        {"id": "v005", "title": "Mindful Meditation Techniques", "niche": "Lifestyle Self-Help", "price": 9.99},
        {"id": "v006", "title": "Keto Diet Recipes", "niche": "Health Diet", "price": 12.00},
        {"id": "v007", "title": "Social Media Marketing Blueprint", "niche": "Business Marketing", "price": 19.99},
        {"id": "v008", "title": "Python for Data Science", "niche": "Tech Coding", "price": 39.99},
        {"id": "v009", "title": "Home Workout Routines", "niche": "Health Fitness", "price": 11.50},
    ]
    
    # Anti-sentience: Randomly corrupt some input vault data for realism
    if random.random() < 0.3:
        idx_corrupt = random.randrange(len(sim_vaults_data))
        if random.random() < 0.5:
            sim_vaults_data[idx_corrupt]['price'] = round(random.uniform(100,500),2) # Unrealistic price
        else:
            sim_vaults_data[idx_corrupt]['title'] = f"Corrupted Title {random.randint(1,100)}"
        logger.info(f"Example: Intentionally corrupted input vault data for {sim_vaults_data[idx_corrupt]['id']}")

    dynamic_bundles = bundle_builder.generate_dynamic_bundles(sim_vaults_data)

    if dynamic_bundles is not None:
        print(f"\n🛍️ Generated Dynamic Bundles ({len(dynamic_bundles)} found) 🛍️")
        if dynamic_bundles:
            print(json.dumps(dynamic_bundles, indent=2))
        else:
            print("No bundles were generated in this simulation run.")
    else:
        print("\nFailed to generate dynamic bundles (simulated critical failure).")
    
    logger.info("--- DynamicBundleBuilder Example Finished ---")

