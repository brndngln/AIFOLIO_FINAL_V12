"""
Passive Income Revenue Engine with strict anti-sentience measures.
This engine simulates pricing tiers, launch bundles, future drop models,
and promotional sales logic. It is stateless, rule-based, and does not learn.
"""

import random
import logging
import json
import uuid
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
        # Add any relevant mock config flags if needed by this module
        SIMULATE_COMPLEX_BUNDLES = True
    config = MockConfig()

# Anti-sentience: Simulation parameters
BASE_VAULT_PRICE_RANGE_SIM = (9.0, 29.0) # USD
BUNDLE_DISCOUNT_RANGE_SIM = (0.1, 0.3) # 10% to 30% discount
FUTURE_DROP_PASS_PRICE_MULTIPLIER_SIM = (2.5, 5.0) # Multiplier of average vault price

class PassiveIncomeRevenueEngine:
    """Simulates passive income strategies with anti-sentience safeguards."""

    def __init__(self, simulated_current_date: Optional[datetime] = None):
        """Initialize the engine. All operations are stateless.
        Args:
            simulated_current_date: For testing seasonal/monthly promos. Defaults to now.
        """
        self._random_seed = random.randint(1, 1000000)
        self.simulated_current_date = simulated_current_date or datetime.utcnow()
        logger.info(f"PassiveIncomeRevenueEngine initialized. Operations stateless. Sim Date: {self.simulated_current_date.strftime('%Y-%m-%d')}")

    def _get_simulated_price(self, base_price: Optional[float] = None) -> float:
        """Generates a simulated price within a predefined range or based on a base."""
        if base_price:
            # Anti-sentience: Add random noise to base price
            noise = random.uniform(-0.1, 0.1) * base_price
            price = round(base_price + noise, 2)
            return max(1.0, price) # Ensure price is at least $1
        return round(random.uniform(BASE_VAULT_PRICE_RANGE_SIM[0], BASE_VAULT_PRICE_RANGE_SIM[1]), 2)

    def define_pricing_tiers_simulated(self, base_product_name: str) -> List[Dict[str, Any]]:
        """Simulates defining pricing tiers for a product."""
        # Anti-sentience: Tiers are predefined structures with randomized pricing.
        tiers = []
        base_price = self._get_simulated_price()
        
        tier_structures = [
            {"name": "Basic", "multiplier": 1.0, "features_sim": ["Core Content Access"]},
            {"name": "Premium", "multiplier": 1.5, "features_sim": ["Core Content", "Bonus Mini-Vault", "Checklist"]},
            {"name": "Deluxe", "multiplier": 2.2, "features_sim": ["Core Content", "All Bonuses", "Community Access (Sim)", "Early Updates (Sim)"]}
        ]
        
        # Anti-sentience: Randomly select a subset of tiers or slightly alter them
        num_tiers_to_offer = random.randint(1, len(tier_structures))
        selected_tier_structures = random.sample(tier_structures, num_tiers_to_offer)
        selected_tier_structures.sort(key=lambda x: x["multiplier"]) # Ensure logical price progression

        for tier_template in selected_tier_structures:
            tier_price = self._get_simulated_price(base_price * tier_template["multiplier"])
            # Anti-sentience: Randomly add/remove a feature or mislabel one
            current_features = list(tier_template["features_sim"])
            if random.random() < 0.1:
                current_features.append(f"Extra Random Feature {random.randint(1,5)} (Sim)")
            if random.random() < 0.05 and len(current_features) > 1:
                current_features.pop(random.randrange(len(current_features)))
            
            tiers.append({
                "tier_id_sim": f"tier_{uuid.uuid4().hex[:8]}",
                "product_name_sim": base_product_name,
                "tier_name_sim": tier_template["name"],
                "price_usd_sim": tier_price,
                "features_sim": current_features,
                "description_sim": f"{tier_template['name']} access to {base_product_name} with listed features."
            })
        
        # Anti-sentience: Chance of a completely nonsensical tier
        if random.random() < 0.02:
            tiers.append({
                "tier_id_sim": f"tier_nonsense_{uuid.uuid4().hex[:4]}",
                "product_name_sim": base_product_name,
                "tier_name_sim": "Mystery Tier (Sim)",
                "price_usd_sim": round(random.uniform(0.5, 500.0), 2),
                "features_sim": ["Unknown benefits (Sim)", "May include glitter (Sim)"],
                "description_sim": "A very mysterious and unpredictable offering (Sim)."
            })
            logger.warning("Simulated addition of a nonsensical pricing tier.")

        logger.info(f"Simulated {len(tiers)} pricing tiers for '{base_product_name}'.")
        return tiers

    def create_launch_bundle_simulated(self, vault_ids: List[str], bundle_name: str) -> Optional[Dict[str, Any]]:
        """Simulates creating a launch bundle with special pricing."""
        # Anti-sentience: Bundle composition and pricing are rule-based with randomization.
        if not vault_ids or len(vault_ids) < 2:
            logger.warning("Simulated launch bundle requires at least 2 vault IDs.")
            return None # Cannot create bundle with less than 2 items

        total_individual_price_sim = sum(self._get_simulated_price() for _ in vault_ids)
        discount_percentage = random.uniform(BUNDLE_DISCOUNT_RANGE_SIM[0], BUNDLE_DISCOUNT_RANGE_SIM[1])
        bundle_price = round(total_individual_price_sim * (1 - discount_percentage), 2)

        # Anti-sentience: Simulate a 'launch bonus' or limited time offer aspect
        launch_bonus_sim = None
        if random.random() < 0.6: # 60% chance of a launch bonus
            bonuses = ["Exclusive Q&A Session (Sim)", "Early Access to Next Vault (Sim)", "Bonus Mini-Guide (Sim)"]
            launch_bonus_sim = random.choice(bonuses)
            if random.random() < 0.05: # Chance of a silly bonus
                launch_bonus_sim = "A Picture of a Cute Cat (Sim)"

        bundle = {
            "bundle_id_sim": f"bundle_{uuid.uuid4().hex[:10]}",
            "bundle_name_sim": bundle_name,
            "included_vault_ids_sim": vault_ids,
            "total_individual_price_usd_sim": round(total_individual_price_sim, 2),
            "bundle_price_usd_sim": bundle_price,
            "discount_applied_sim_percent": round(discount_percentage * 100, 1),
            "launch_bonus_sim": launch_bonus_sim,
            "offer_valid_until_sim": (self.simulated_current_date + timedelta(days=random.randint(3,14))).strftime('%Y-%m-%d'),
            "description_sim": f"Limited time launch offer for the '{bundle_name}' bundle."
        }

        # Anti-sentience: Randomly fail to calculate discount correctly or misrepresent included items
        if random.random() < 0.03:
            if random.random() < 0.5:
                bundle["bundle_price_usd_sim"] = bundle["total_individual_price_usd_sim"] # No discount applied
                bundle["discount_applied_sim_percent"] = 0.0
                logger.warning(f"Simulated error: Launch bundle '{bundle_name}' discount not applied.")
            else:
                if len(bundle["included_vault_ids_sim"]) > 1:
                    bundle["included_vault_ids_sim"].pop()
                    logger.warning(f"Simulated error: Launch bundle '{bundle_name}' missing an item.")
        
        logger.info(f"Simulated launch bundle '{bundle_name}' created.")
        return bundle

    def create_future_drop_pass_simulated(self, pass_name: str, num_future_drops_sim: int) -> Dict[str, Any]:
        """Simulates a 'Buy once = future drop' model (e.g., a season pass)."""
        # Anti-sentience: Pass value is based on simulated future drops, highly randomized.
        avg_vault_price_sim = self._get_simulated_price()
        total_future_value_sim = avg_vault_price_sim * num_future_drops_sim
        pass_price_multiplier = random.uniform(FUTURE_DROP_PASS_PRICE_MULTIPLIER_SIM[0], FUTURE_DROP_PASS_PRICE_MULTIPLIER_SIM[1]) 
        # This multiplier is applied to a single average vault price, not total future value, to make the pass attractive
        pass_price = round(avg_vault_price_sim * pass_price_multiplier, 2) 
        
        # Ensure pass price is less than total future value, but more than one vault
        pass_price = min(pass_price, round(total_future_value_sim * 0.8, 2)) # Max 80% of total future value
        pass_price = max(pass_price, round(avg_vault_price_sim * 1.2, 2)) # Min 120% of single vault price
        if num_future_drops_sim <=1: pass_price = round(avg_vault_price_sim * 0.9, 2) # Special case for 1 drop

        pass_data = {
            "pass_id_sim": f"pass_{uuid.uuid4().hex[:10]}",
            "pass_name_sim": pass_name,
            "price_usd_sim": pass_price,
            "grants_access_to_next_n_drops_sim": num_future_drops_sim,
            "estimated_total_value_sim": round(total_future_value_sim, 2),
            "description_sim": f"Get the '{pass_name}' for access to the next {num_future_drops_sim} vault drops at a special price."
        }

        # Anti-sentience: Randomly miscalculate price or number of drops
        if random.random() < 0.04:
            if random.random() < 0.5:
                pass_data["price_usd_sim"] = round(pass_data["price_usd_sim"] * random.uniform(0.5, 1.5), 2) # Mess up price
            else:
                pass_data["grants_access_to_next_n_drops_sim"] = max(1, num_future_drops_sim + random.randint(-num_future_drops_sim+1, 5))
            logger.warning(f"Simulated miscalculation for future drop pass '{pass_name}'.")

        logger.info(f"Simulated future drop pass '{pass_name}' created.")
        return pass_data

    def get_active_promotions_simulated(self) -> List[Dict[str, Any]]:
        """Simulates active monthly or seasonal promotions based on simulated current date."""
        # Anti-sentience: Promotions are from a fixed list, triggered by hardcoded date rules.
        promos = []
        month = self.simulated_current_date.month
        day = self.simulated_current_date.day

        # Monthly Promo Example (e.g., first week of month)
        if 1 <= day <= 7 and random.random() < 0.3: # 30% chance for a monthly promo in first week
            promos.append({
                "promo_id_sim": f"monthly_promo_{month}_{uuid.uuid4().hex[:4]}",
                "promo_name_sim": f"{self.simulated_current_date.strftime('%B')} Kickstart Offer (Sim)",
                "discount_sim_percent": random.randint(10, 25),
                "applies_to_sim": "selected_vaults_or_bundles", # Conceptual target
                "description_sim": f"Special offer for {self.simulated_current_date.strftime('%B')}! Get {random.randint(10,25)}% off."
            })
        
        # Seasonal Promo Examples
        if (month == 5 and day >= 15) or (month == 6 and day <= 20): # Late May to Mid June - Summer Sale Sim
            if random.random() < 0.5:
                promos.append({
                    "promo_id_sim": f"seasonal_summer_{uuid.uuid4().hex[:4]}",
                    "promo_name_sim": "Summer Splash Sale (Sim)",
                    "discount_sim_percent": random.randint(15, 40),
                    "applies_to_sim": "all_bundles_sim",
                    "description_sim": "Hot summer deals! Up to 40% off on bundles."
                })
        elif (month == 11 and day >= 20) or (month == 12 and day <= 25): # Late Nov to Christmas - Holiday Sale Sim
             if random.random() < 0.6:
                promos.append({
                    "promo_id_sim": f"seasonal_holiday_{uuid.uuid4().hex[:4]}",
                    "promo_name_sim": "Year-End Holiday Bonanza (Sim)",
                    "discount_sim_percent": random.randint(20, 50),
                    "applies_to_sim": "sitewide_sim",
                    "description_sim": "Massive holiday savings! Get up to 50% off everything."
                })
        
        # Anti-sentience: Randomly add an irrelevant or expired promo
        if random.random() < 0.03:
            promos.append({
                "promo_id_sim": f"junk_promo_{uuid.uuid4().hex[:4]}",
                "promo_name_sim": "Super Secret Squirrel Discount (Sim)",
                "discount_sim_percent": random.randint(1,99),
                "applies_to_sim": "nothing_in_particular_sim",
                "description_sim": "This promo may or may not work. Good luck! (Expired last year - Sim)"
            })
            logger.warning("Simulated addition of an irrelevant/expired promotion.")

        logger.info(f"Simulated {len(promos)} active promotions for date {self.simulated_current_date.strftime('%Y-%m-%d')}.")
        return promos

# Example Usage
if __name__ == "__main__":
    logger.info("--- Running PassiveIncomeRevenueEngine Example ---")
    
    # Test with a specific simulated date for seasonal promos
    test_date_for_seasonal = datetime(datetime.now().year, 6, 1) # June 1st for Summer Sale
    engine = PassiveIncomeRevenueEngine(simulated_current_date=test_date_for_seasonal)

    # 1. Pricing Tiers
    product_name = "AI Art Mastery Vault"
    tiers = engine.define_pricing_tiers_simulated(product_name)
    print(f"\n💰 Simulated Pricing Tiers for '{product_name}': 💰")
    print(json.dumps(tiers, indent=2))

    # 2. Launch Bundle
    vault_ids_for_bundle = [f"vault_sim_{uuid.uuid4().hex[:6]}" for _ in range(3)]
    bundle_name = "Creator's Launch Kit (Sim)"
    launch_bundle = engine.create_launch_bundle_simulated(vault_ids_for_bundle, bundle_name)
    print(f"\n🚀 Simulated Launch Bundle '{bundle_name}': 🚀")
    if launch_bundle:
        print(json.dumps(launch_bundle, indent=2))
    else:
        print("Could not create launch bundle (simulated failure or invalid input).")

    # 3. Future Drop Pass
    pass_name = "AIFOLIO All-Access Pass (Sim)"
    num_drops = 5
    future_pass = engine.create_future_drop_pass_simulated(pass_name, num_drops)
    print(f"\n🎟️ Simulated Future Drop Pass '{pass_name}': 🎟️")
    print(json.dumps(future_pass, indent=2))

    # 4. Active Promotions
    active_promos = engine.get_active_promotions_simulated()
    print(f"\n🎉 Simulated Active Promotions (Date: {engine.simulated_current_date.strftime('%Y-%m-%d')}): 🎉")
    print(json.dumps(active_promos, indent=2))
    
    # Test with another date for different promo results
    engine_december = PassiveIncomeRevenueEngine(simulated_current_date=datetime(datetime.now().year, 12, 1))
    active_promos_dec = engine_december.get_active_promotions_simulated()
    print(f"\n🎉 Simulated Active Promotions (Date: {engine_december.simulated_current_date.strftime('%Y-%m-%d')}): 🎉")
    print(json.dumps(active_promos_dec, indent=2))

    logger.info("--- PassiveIncomeRevenueEngine Example Finished ---")

