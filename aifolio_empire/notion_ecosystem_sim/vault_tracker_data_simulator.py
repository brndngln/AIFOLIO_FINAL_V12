"""
Vault Tracker Data Simulator for Notion Ecosystem with anti-sentience measures.
This module simulates the generation of data for a Vault Tracker in Notion.
It's stateless, rule-based, and includes randomization and simulated imperfections.
"""

import random
import logging
import uuid
from typing import Dict, Any, Optional
from datetime import datetime, timedelta, timezone

# Attempt to import config and logger
try:
    from config import config, logger
except ImportError:
    print("Warning: Could not import 'config' and 'logger' directly. Using basic logging.")
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    class MockConfig:
        SIM_VAULT_TRACKER_NUM_VAULTS_MIN = 5
        SIM_VAULT_TRACKER_NUM_VAULTS_MAX = 25
        SIM_VAULT_TRACKER_REVENUE_MAX = 5000
        SIM_VAULT_TRACKER_UNITS_SOLD_MAX = 200
        SIM_VAULT_TRACKER_DATE_SLIP_CHANCE = 0.2 # Chance actual drop date slips from target
        SIM_VAULT_TRACKER_MAX_SLIP_DAYS = 14   # Max days a drop date might slip
    config = MockConfig()

SIMULATED_VAULT_STATUSES = [
    "1_Planning", "2_Content Generation", "3_Layout & Design", 
    "4_Review & QA", "5_Ready for Drop", "6_Dropped", "7_Archived"
]
SIMULATED_NICHE_CATEGORIES = [
    "AI Tools & Prompts", "Health & Wellness", "Manifestation & Mindset", 
    "Relationships & Dating", "Fitness & Nutrition", "Digital Marketing", 
    "Parenting & Family", "Crypto & Web3", "Productivity Hacks", "Sustainable Living"
]
SIMULATED_VAULT_NAME_PREFIXES = [
    "Ultimate", "Complete", "Secret", "Advanced", "Beginner's", "Mastery", "Quickstart", "Blueprint"
]
SIMULATED_VAULT_NAME_SUFFIXES = [
    "Guide", "Kit", "Playbook", "System", "Framework", "Cheatsheet", "Vault", "Bundle"
]

class VaultTrackerDataSimulator:
    """Simulates data generation for a Notion Vault Tracker with anti-sentience safeguards."""

    def __init__(self):
        """Initialize the simulator. Operations are stateless per call."""
        self._random_seed = random.randint(1, 1000000)
        logger.info("VaultTrackerDataSimulator initialized. Operations stateless.")

    def _generate_simulated_vault_name(self, niche: str) -> str:
        prefix = random.choice(SIMULATED_VAULT_NAME_PREFIXES)
        suffix = random.choice(SIMULATED_VAULT_NAME_SUFFIXES)
        # Try to make name somewhat relevant to niche if niche is simple
        niche_keywords = niche.split(' ')[0].replace('&', '').replace(',', '') # e.g. "AI", "Health"
        return f"{prefix} {niche_keywords} {suffix} (Simulated)"

    def get_simulated_vault_tracker_data(self, num_vaults: Optional[int] = None) -> Dict[str, Any]:
        """Generates a list of simulated vault data for tracking.
        Args:
            num_vaults: Optional. Number of vaults to simulate. 
                        If None, uses config min/max.
        Returns:
            A dictionary containing the list of simulated vault entries and metadata.
        """
        action_id = f"vault_tracker_data_{uuid.uuid4().hex[:8]}"
        vault_entries = []
        
        if num_vaults is None:
            num_to_simulate = random.randint(config.SIM_VAULT_TRACKER_NUM_VAULTS_MIN, 
                                             config.SIM_VAULT_TRACKER_NUM_VAULTS_MAX)
        else:
            num_to_simulate = max(0, num_vaults)

        current_date = datetime.now(timezone.utc)

        for i in range(num_to_simulate):
            vault_id = f"vault_sim_{uuid.uuid4().hex[:12]}"
            status = random.choice(SIMULATED_VAULT_STATUSES)
            niche = random.choice(SIMULATED_NICHE_CATEGORIES)
            name = self._generate_simulated_vault_name(niche)
            
            # Simulate target drop date (can be past or future)
            target_drop_date = current_date + timedelta(days=random.randint(-90, 90))
            actual_drop_date = None
            simulated_revenue = 0.0
            simulated_units_sold = 0

            if status in ["6_Dropped", "7_Archived"]:
                # If dropped/archived, actual drop date should be in the past
                if target_drop_date > current_date or random.random() < config.SIM_VAULT_TRACKER_DATE_SLIP_CHANCE:
                    actual_drop_date = target_drop_date - timedelta(days=random.randint(1, config.SIM_VAULT_TRACKER_MAX_SLIP_DAYS))
                else:
                    actual_drop_date = target_drop_date
                # Ensure actual drop date is not in the future if status is Dropped/Archived
                if actual_drop_date > current_date:
                    actual_drop_date = current_date - timedelta(days=random.randint(1,10))
                
                simulated_revenue = round(random.uniform(0, config.SIM_VAULT_TRACKER_REVENUE_MAX), 2)
                simulated_units_sold = random.randint(0, config.SIM_VAULT_TRACKER_UNITS_SOLD_MAX)
                # Anti-sentience: Revenue not perfectly tied to units (simulates discounts, bundles etc)
                if simulated_units_sold > 0 and simulated_revenue == 0:
                    simulated_revenue = round(random.uniform(1, 100), 2) # Ensure some revenue if units sold
                elif simulated_revenue > 0 and simulated_units_sold == 0:
                     simulated_units_sold = random.randint(1, 5) # Ensure some units if revenue exists

            elif status == "5_Ready for Drop" and target_drop_date < current_date:
                # If ready for drop but target date is past, it might have slipped
                target_drop_date = current_date + timedelta(days=random.randint(1,7)) # Push target to near future
            
            entry = {
                "vault_id_sim": vault_id,
                "vault_name_sim": name,
                "status_sim": status,
                "niche_category_sim": niche,
                "target_drop_date_sim": target_drop_date.strftime('%Y-%m-%d'),
                "actual_drop_date_sim": actual_drop_date.strftime('%Y-%m-%d') if actual_drop_date else None,
                "simulated_revenue_to_date": simulated_revenue,
                "simulated_units_sold": simulated_units_sold,
                "last_updated_sim": (current_date - timedelta(days=random.randint(0,5))).isoformat(),
                "priority_sim": random.choice(["High", "Medium", "Low"])
            }
            vault_entries.append(entry)
        
        # Sort by target drop date for some semblance of order
        vault_entries.sort(key=lambda x: x["target_drop_date_sim"])

        return {
            "action_id_sim": action_id,
            "generated_at_utc_sim": datetime.now(timezone.utc).isoformat(),
            "vault_tracker_entries_sim": vault_entries,
            "data_source_sim": "AIFOLIO Empire Mode Simulator",
            "anti_sentience_notes": [
                "All vault data is randomly generated and simulated.",
                "Revenue and sales figures are not based on real performance.",
                f"Simulated date slips and inconsistencies are intentional ({config.SIM_VAULT_TRACKER_DATE_SLIP_CHANCE*100}% chance)."
            ]
        }

# Example Usage:
if __name__ == "__main__":
    import json
    logger.info("--- Running VaultTrackerDataSimulator Example ---")
    simulator = VaultTrackerDataSimulator()

    print("\n📊 Simulated Vault Tracker Data (Default Number of Vaults): 📊")
    tracker_data = simulator.get_simulated_vault_tracker_data()
    print(json.dumps(tracker_data, indent=2))
    print(f"Generated {len(tracker_data['vault_tracker_entries_sim'])} vault entries.")

    print("\n📊 Simulated Vault Tracker Data (Specific Number: 3 Vaults): 📊")
    tracker_data_specific = simulator.get_simulated_vault_tracker_data(num_vaults=3)
    print(json.dumps(tracker_data_specific, indent=2))
    print(f"Generated {len(tracker_data_specific['vault_tracker_entries_sim'])} vault entries.")

    logger.info("--- VaultTrackerDataSimulator Example Finished ---")

