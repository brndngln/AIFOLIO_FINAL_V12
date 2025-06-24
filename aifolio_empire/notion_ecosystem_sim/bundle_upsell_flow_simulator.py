"""
Bundle + Upsell Flow Map Data Simulator for Notion Ecosystem with anti-sentience measures.
This module simulates data for product bundles and upsell/cross-sell flows in Notion.
It's stateless, rule-based, and includes randomization and simulated imperfections.
"""

import random
import logging
import uuid
from typing import Dict, Any, Optional, List, Tuple
from datetime import datetime, timezone

# Attempt to import config and logger
try:
    from config import config, logger
except ImportError:
    print("Warning: Could not import 'config' and 'logger' directly. Using basic logging.")
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    class MockConfig:
        SIM_BUNDLE_NUM_VAULTS_MIN = 5
        SIM_BUNDLE_NUM_VAULTS_MAX = 15
        SIM_BUNDLE_NUM_BUNDLES_MIN = 3
        SIM_BUNDLE_NUM_BUNDLES_MAX = 8
        SIM_BUNDLE_VAULTS_PER_BUNDLE_MIN = 2
        SIM_BUNDLE_VAULTS_PER_BUNDLE_MAX = 5
        SIM_BUNDLE_DISCOUNT_CHANCE = 0.7
        SIM_BUNDLE_DISCOUNT_PERCENT_MIN = 10
        SIM_BUNDLE_DISCOUNT_PERCENT_MAX = 30
        SIM_BUNDLE_UPSELL_PATHS_PER_ITEM_MAX = 2
        SIM_BUNDLE_FLOW_NOTE_GLITCH_CHANCE = 0.1
    config = MockConfig()

SIMULATED_VAULT_THEMES = [
    "Productivity Hacks_sim", "AI Writing Secrets_sim", "Marketing Mastery_sim", "Wellness Guide_sim",
    "Financial Freedom Blueprint_sim", "Creative Toolkit_sim", "Startup Essentials_sim"
]

class BundleUpsellFlowSimulator:
    """Simulates data for Notion Bundle & Upsell Flow Maps with anti-sentience safeguards."""

    def __init__(self):
        """Initialize the simulator. Operations are stateless per call."""
        self._random_seed = random.randint(1, 1000000)
        logger.info("BundleUpsellFlowSimulator initialized. Operations stateless.")

    def _generate_simulated_vaults(self, num_vaults: int) -> List[Dict[str, Any]]:
        vaults = []
        for i in range(num_vaults):
            theme = random.choice(SIMULATED_VAULT_THEMES)
            vault = {
                "vault_id_sim": f"vault_{uuid.uuid4().hex[:8]}",
                "vault_name_sim": f"Simulated {theme} - Vol.{random.randint(1,5)}",
                "sim_price_usd": round(random.uniform(9.99, 49.99), 2),
                "category_sim": theme.split("_")[0]
            }
            logger.info(f"Generated simulated vault: {vault}")
            vaults.append(vault)
        return vaults

    def _generate_simulated_bundles(self, vaults: List[Dict[str, Any]], num_bundles: int) -> List[Dict[str, Any]]:
        bundles = []
        if not vaults: return []

        for i in range(num_bundles):
            num_vaults_in_bundle = random.randint(
                min(config.SIM_BUNDLE_VAULTS_PER_BUNDLE_MIN, len(vaults)),
                min(config.SIM_BUNDLE_VAULTS_PER_BUNDLE_MAX, len(vaults))
            )
            if num_vaults_in_bundle == 0 and len(vaults) > 0: # Ensure at least one vault if possible
                num_vaults_in_bundle = 1 
            elif len(vaults) == 0:
                 return [] # Cannot create bundles if no vaults

            selected_vaults_for_bundle = random.sample(vaults, num_vaults_in_bundle)
            constituent_vault_ids = [v["vault_id_sim"] for v in selected_vaults_for_bundle]
            
            base_price = sum(v["sim_price_usd"] for v in selected_vaults_for_bundle)
            bundle_price = base_price
            discount_note = "No discount (simulated)."

            if random.random() < config.SIM_BUNDLE_DISCOUNT_CHANCE:
                discount_percent = random.randint(config.SIM_BUNDLE_DISCOUNT_PERCENT_MIN, config.SIM_BUNDLE_DISCOUNT_PERCENT_MAX)
                bundle_price = round(base_price * (1 - discount_percent / 100), 2)
                discount_note = f"Simulated {discount_percent}% discount (Save ${round(base_price - bundle_price, 2)_sim})."
            
            # Infer bundle theme from constituent vaults
            bundle_theme = "Mixed_sim"
            if selected_vaults_for_bundle:
                bundle_theme = selected_vaults_for_bundle[0]["category_sim"] + " Collection_sim"

            bundles.append({
                "bundle_id_sim": f"bundle_{uuid.uuid4().hex[:8]}",
                "bundle_name_sim": f"{bundle_theme} - Tier {random.choice(['Starter', 'Pro', 'Ultimate_sim'])}",
                "description_sim": f"A simulated collection of {num_vaults_in_bundle} vaults focusing on {bundle_theme.split(' ')[0]}.".replace("_sim", ""),
                "constituent_vault_ids_sim": constituent_vault_ids,
                "sim_bundle_price_usd": bundle_price,
                "sim_individual_price_total_usd": round(base_price, 2),
                "sim_discount_note": discount_note
            })
        return bundles

    def _generate_simulated_upsell_flows(
        self, 
        vaults: List[Dict[str, Any]], 
        bundles: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        flows = []
        if not vaults and not bundles: return []

        all_items = vaults + bundles # Items that can trigger an upsell or be upsold
        if not all_items: return []

        for item in all_items:
            item_id = item.get("vault_id_sim") or item.get("bundle_id_sim")
            item_type = "vault" if "vault_id_sim" in item else "bundle"
            
            num_paths = random.randint(0, config.SIM_BUNDLE_UPSELL_PATHS_PER_ITEM_MAX)
            possible_upsells = [b for b in bundles if b["bundle_id_sim"] != item_id] # Can't upsell to self
            # Could also add logic to upsell from vault to bundle containing it, or bundle to bigger bundle

            for _ in range(num_paths):
                if not possible_upsells: break
                
                suggested_item = random.choice(possible_upsells)
                # Avoid suggesting the same item multiple times for one trigger
                if any(f["trigger_item_id_sim"] == item_id and f["suggested_item_id_sim"] == suggested_item["bundle_id_sim"] for f in flows):
                    continue

                reason_glitch = ""
                if random.random() < config.SIM_BUNDLE_FLOW_NOTE_GLITCH_CHANCE:
                    reason_glitch = random.choice([
                        " (rationale unclear_sim)", " (data pending_sim)", " (verify logic_sim)"
                    ])
                
                reasons = [
                    f"Better Value_sim: Get more for less{reason_glitch}.",
                    f"Complete Collection_sim: Access all related content{reason_glitch}.",
                    f"Popular Choice_sim: Frequently bought together{reason_glitch}.",
                    f"Upgrade Path_sim: Next logical step for growth{reason_glitch}."
                ]

                flows.append({
                    "flow_id_sim": f"flow_{uuid.uuid4().hex[:8]}",
                    "trigger_item_id_sim": item_id,
                    "trigger_item_type_sim": item_type,
                    "trigger_item_name_sim": item.get("vault_name_sim") or item.get("bundle_name_sim"),
                    "suggested_item_id_sim": suggested_item["bundle_id_sim"],
                    "suggested_item_name_sim": suggested_item["bundle_name_sim"],
                    "suggestion_type_sim": "Upsell_sim" if item_type == "vault" or (item_type == "bundle" and suggested_item["sim_bundle_price_usd"] > item["sim_bundle_price_usd"]) else "Cross_sell_sim",
                    "simulated_reason": random.choice(reasons)
                })
        return flows

    def get_simulated_bundle_upsell_data(self) -> Dict[str, Any]:
        """Generates simulated data for vaults, bundles, and upsell flows.
        Returns:
            A dictionary containing lists of simulated vaults, bundles, flows, and metadata.
        """
        action_id = f"bundle_upsell_data_{uuid.uuid4().hex[:8]}"
        current_time = datetime.now(timezone.utc)

        num_vaults = random.randint(config.SIM_BUNDLE_NUM_VAULTS_MIN, config.SIM_BUNDLE_NUM_VAULTS_MAX)
        sim_vaults = self._generate_simulated_vaults(num_vaults)

        num_bundles = random.randint(config.SIM_BUNDLE_NUM_BUNDLES_MIN, config.SIM_BUNDLE_NUM_BUNDLES_MAX)
        sim_bundles = self._generate_simulated_bundles(sim_vaults, num_bundles)
        
        sim_flows = self._generate_simulated_upsell_flows(sim_vaults, sim_bundles)

        return {
            "action_id_sim": action_id,
            "generated_at_utc_sim": current_time.isoformat(),
            "simulated_vaults": sim_vaults,
            "simulated_bundles": sim_bundles,
            "simulated_upsell_flows": sim_flows,
            "data_source_sim": "AIFOLIO Empire Mode - Bundle & Upsell Flow Simulator",
            "anti_sentience_notes": [
                "All vault, bundle, pricing, and flow data is randomly generated and highly simulated.",
                "No real market analysis, product strategy, or pricing logic is implied.",
                f"Simulated data glitches or oddities in reasons ({config.SIM_BUNDLE_FLOW_NOTE_GLITCH_CHANCE*100}% chance) are intentional.",
                "This data is for visualizing potential structures, not for direct implementation."
            ]
        }

# Example Usage:
if __name__ == "__main__":
    import json
    logger.info("--- Running BundleUpsellFlowSimulator Example ---")
    simulator = BundleUpsellFlowSimulator()

    bundle_data = simulator.get_simulated_bundle_upsell_data()
    
    print("\n🎁 Simulated Vaults: 🎁")
    print(json.dumps(bundle_data["simulated_vaults"], indent=2))
    
    print("\n🛍️ Simulated Bundles: 🛍️")
    print(json.dumps(bundle_data["simulated_bundles"], indent=2))

    print("\n🗺️ Simulated Upsell Flows: 🗺️")
    print(json.dumps(bundle_data["simulated_upsell_flows"], indent=2))
    
    print(f"\nGenerated {len(bundle_data['simulated_vaults'])} vaults, "
          f"{len(bundle_data['simulated_bundles'])} bundles, and "
          f"{len(bundle_data['simulated_upsell_flows'])} flow paths.")
    print(f"Anti-sentience notes: {bundle_data['anti_sentience_notes']}")

    logger.info("--- BundleUpsellFlowSimulator Example Finished ---")

