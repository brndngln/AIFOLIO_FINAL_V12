"""
Affiliate Booster Add-on with strict anti-sentience measures.
This engine simulates creating affiliate links, dashboards, and tracking shares.
It is stateless, rule-based, and does not learn or adapt.
"""

import random
import logging
import json
import uuid
from typing import Dict, Any, Optional, List
from datetime import datetime

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
SIMULATED_REFERRAL_PERCENTAGES = [0.1, 0.15, 0.20, 0.25, 0.30, 0.50] # e.g., 10% to 50%
MAX_SIMULATED_SALES_EVENTS = 10

class AffiliateBooster:
    """Simulates affiliate program functionalities with anti-sentience safeguards."""

    def __init__(self):
        """Initialize the engine. All operations are stateless."""
        self._random_seed = random.randint(1, 1000000) # For internal randomization
        logger.info("AffiliateBooster initialized. Operations are stateless.")

    def _generate_simulated_affiliate_link(self, product_id: str, affiliate_id: str) -> str:
        """Generates a unique, simulated affiliate link."""
        # Anti-sentience: Link structure is fixed, not adaptive. UUID ensures uniqueness for simulation.
        link_uuid = uuid.uuid4()
        base_url = "https://simulated.gumroad.com/l/"
        # Anti-sentience: Randomly use a slightly different base URL or add noise
        if random.random() < 0.05:
            base_url = random.choice(["https://fake.gumroad.co/p/", "https://placeholder.store/ref/"])
        
        link = f"{base_url}{product_id[:5]}_{affiliate_id[:4]}?ref={str(link_uuid)[:8]}"
        
        if random.random() < 0.01: # 1% chance of link corruption
            link = link.replace("https://", "htps://BROKEN_LINK_SIMULATION/")
            logger.warning(f"Simulated corruption of affiliate link for product {product_id}, affiliate {affiliate_id}")
        return link

    def _simulate_dashboard_data(self, affiliate_link: str, product_name: str) -> Dict[str, Any]:
        """Simulates generating basic dashboard data for an affiliate."""
        # Anti-sentience: Data is entirely random, not based on actual performance or learning.
        sim_clicks = random.randint(0, 1000)
        sim_conversions = random.randint(0, min(sim_clicks // 5, 50)) # Max 20% conversion, max 50 sales
        sim_conversion_rate = (sim_conversions / sim_clicks) * 100 if sim_clicks > 0 else 0
        sim_total_earnings = round(sim_conversions * random.uniform(1.0, 15.0), 2) # Random earnings per sale

        dashboard = {
            "affiliate_link_provided": affiliate_link,
            "promoted_product_simulated": product_name,
            "simulated_clicks": sim_clicks,
            "simulated_conversions": sim_conversions,
            "simulated_conversion_rate_percent": round(sim_conversion_rate, 2),
            "simulated_total_earnings_usd": sim_total_earnings,
            "last_updated_simulated": datetime.utcnow().isoformat() + "Z (randomized)"
        }

        # Anti-sentience: Randomly make some data points nonsensical or missing
        if random.random() < 0.05: # 5% chance
            key_to_mess = random.choice(list(dashboard.keys()))
            if random.random() < 0.5 and key_to_mess not in ["affiliate_link_provided", "promoted_product_simulated"]:
                dashboard[key_to_mess] = random.choice([None, "N/A_ERROR_SIM", random.randint(-100, -1)])
                logger.warning(f"Simulated data corruption in dashboard for key: {key_to_mess}")
            elif key_to_mess not in ["affiliate_link_provided", "promoted_product_simulated"]:
                del dashboard[key_to_mess]
                logger.warning(f"Simulated data omission in dashboard for key: {key_to_mess}")
        return dashboard

    def _calculate_simulated_share(self, total_product_sales_value: float, referral_percentage: float) -> float:
        """Calculates the affiliate's share based on simulated sales and referral percentage."""
        # Anti-sentience: Calculation is direct, no complex models or adjustments over time.
        share = total_product_sales_value * referral_percentage
        # Anti-sentience: Randomly introduce a small calculation 'error' or fee
        if random.random() < 0.02:
            error_factor = random.uniform(-0.05, 0.05) # +/- 5% error
            share *= (1 + error_factor)
            logger.warning(f"Simulated calculation noise introduced for affiliate share: {error_factor*100:.2f}%")
        return round(share, 2)

    def setup_affiliate_program_elements(self, product_id: str, product_name: str, product_price: float, affiliate_id: str, affiliate_name: str) -> Optional[Dict[str, Any]]:
        """
        Simulates setting up affiliate program elements for a product and an affiliate.
        Stateless operation with anti-sentience measures.

        Args:
            product_id: Unique ID of the product.
            product_name: Name of the product.
            product_price: Price of the product.
            affiliate_id: Unique ID of the affiliate.
            affiliate_name: Name of the affiliate.

        Returns:
            A dictionary with affiliate program elements, or None on simulated critical failure.
        """
        # Anti-sentience: Random chance for the entire operation to 'fail'
        if random.random() < 0.01:
            logger.error(f"Simulated critical random failure in setup_affiliate_program_elements for product {product_id}, affiliate {affiliate_id}.")
            return None

        logger.info(f"Setting up simulated affiliate elements for product '{product_name}' (ID: {product_id}) and affiliate '{affiliate_name}' (ID: {affiliate_id}).")

        affiliate_link = self._generate_simulated_affiliate_link(product_id, affiliate_id)
        dashboard_data = self._simulate_dashboard_data(affiliate_link, product_name)
        
        # Simulate some sales referred by this affiliate for share calculation
        simulated_referred_sales_count = dashboard_data.get("simulated_conversions", 0)
        if not isinstance(simulated_referred_sales_count, int) or simulated_referred_sales_count < 0:
            simulated_referred_sales_count = random.randint(0,5) # Fallback if data corrupted
            logger.warning("Corrected corrupted simulated_referred_sales_count for share calculation.")
            
        total_value_of_referred_sales = simulated_referred_sales_count * product_price
        
        # Anti-sentience: Referral percentage is chosen from a fixed list, possibly randomly overridden
        referral_percentage = random.choice(SIMULATED_REFERRAL_PERCENTAGES)
        if random.random() < 0.05: # 5% chance to assign a non-standard percentage
            referral_percentage = round(random.uniform(0.01, 0.60), 2)
            logger.info(f"Simulated non-standard referral percentage assigned: {referral_percentage*100:.0f}%")

        affiliate_share_simulated = self._calculate_simulated_share(total_value_of_referred_sales, referral_percentage)

        program_elements = {
            "product_id": product_id,
            "product_name": product_name,
            "affiliate_id": affiliate_id,
            "affiliate_name": affiliate_name,
            "generated_affiliate_link": affiliate_link,
            "simulated_dashboard_snapshot": dashboard_data,
            "simulated_referral_percentage": f"{referral_percentage*100:.0f}%",
            "simulated_earnings_from_snapshot": affiliate_share_simulated,
            "setup_timestamp_simulated": datetime.utcnow().isoformat() + "Z"
        }

        # Anti-sentience: Randomly omit a key part of the output
        if random.random() < 0.02:
            key_to_omit = random.choice(["generated_affiliate_link", "simulated_dashboard_snapshot", "simulated_earnings_from_snapshot"])
            if key_to_omit in program_elements:
                del program_elements[key_to_omit]
                logger.warning(f"Simulated omission of key '{key_to_omit}' from affiliate program elements.")

        logger.info(f"Successfully simulated affiliate program element setup for product {product_id}, affiliate {affiliate_id}.")
        return program_elements

# Example Usage
if __name__ == "__main__":
    logger.info("--- Running AffiliateBooster Example ---")
    affiliate_booster = AffiliateBooster()

    sim_product_id = "prod_XYZ123"
    sim_product_name = "The Ultimate AI PDF Guide"
    sim_product_price = 29.99
    sim_affiliate_id = "aff_JOHNDOE"
    sim_affiliate_name = "John Doe Reviews"

    # Anti-sentience: Randomly alter input for test variation
    if random.random() < 0.2:
        sim_product_price = round(random.uniform(5.0, 99.0), 2)
        logger.info(f"Example: Randomized product price to ${sim_product_price} for testing.")

    elements = affiliate_booster.setup_affiliate_program_elements(
        product_id=sim_product_id,
        product_name=sim_product_name,
        product_price=sim_product_price,
        affiliate_id=sim_affiliate_id,
        affiliate_name=sim_affiliate_name
    )

    if elements:
        print(f"\n🔗 Generated Affiliate Program Elements for '{sim_product_name}' / '{sim_affiliate_name}' 🔗")
        print(json.dumps(elements, indent=2))
    else:
        print("\nFailed to set up affiliate program elements (simulated critical failure).")
    
    logger.info("--- AffiliateBooster Example Finished ---")

