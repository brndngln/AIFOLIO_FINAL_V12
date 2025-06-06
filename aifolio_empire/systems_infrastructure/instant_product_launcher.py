"""
Instant Product Launcher Simulator with strict anti-sentience measures.
This module simulates the one-click launching of a vault (digital product)
to a platform like Gumroad, including simulated file upload, price setting,
copy filling, and short link generation.
It is stateless, rule-based, does not make real API calls, and does not learn.
"""

import random
import logging
import json
import uuid
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
import time
import urllib.parse # For simulating URL components

# Attempt to import config and logger
try:
    from config import config, logger
except ImportError:
    print("Warning: Could not import 'config' and 'logger' directly. Using basic logging.")
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    class MockConfig:
        SIMULATED_GUMROAD_BASE_URL = "https://sim-user.gumroad.com/l/"
        SIMULATED_BITLY_BASE_URL = "https://sim.ly/"
        SIMULATED_LAUNCH_FAIL_RATE = 0.05
        SIMULATED_COPY_FILTER_RATE = 0.02
    config = MockConfig()

class InstantProductLauncher:
    """Simulates launching a product to Gumroad with anti-sentience safeguards."""

    def __init__(self):
        """Initialize the simulator. All operations are stateless."""
        self._random_seed = random.randint(1, 1000000)
        logger.info("InstantProductLauncher initialized. Operations stateless. Real platform interactions NOT made.")

    def _simulate_platform_delay(self, min_delay: float = 0.5, max_delay: float = 2.5):
        """Simulates a random platform interaction delay."""
        delay = random.uniform(min_delay, max_delay)
        logger.debug(f"Simulated platform interaction delay of {delay:.2f} seconds.")
        if random.random() < 0.01:
            long_delay = random.uniform(max_delay, max_delay * 3)
            logger.warning(f"Simulated unexpectedly long platform delay of {long_delay:.2f} seconds.")

    def _generate_simulated_short_id(self, length: int = 7) -> str:
        """Generates a random alphanumeric ID for simulated URLs."""
        return ''.join(random.choices("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", k=length))

    def _simulate_file_upload(self, vault_file_name_sim: str) -> Dict[str, Any]:
        """Simulates the file upload process."""
        # Anti-sentience: No actual file is read or transferred.
        if not vault_file_name_sim or not isinstance(vault_file_name_sim, str):
            return {"success": False, "error": "Invalid vault_file_name_sim provided.", "file_id_sim": None}
        
        if random.random() < 0.02: # Simulate upload failure
            logger.warning(f"Simulated file upload failure for: {vault_file_name_sim}")
            return {"success": False, "error": "Simulated network error during upload.", "file_id_sim": None}
        
        sim_file_id = f"file_sim_{uuid.uuid4().hex[:16]}"
        logger.info(f"Simulated successful upload of '{vault_file_name_sim}'. File ID (sim): {sim_file_id}")
        return {"success": True, "message": "File uploaded successfully (simulated).", "file_id_sim": sim_file_id}

    def simulate_product_launch(self, 
                                vault_name: str, 
                                vault_file_name_sim: str, 
                                price_usd: float, 
                                product_description_sim: str,
                                cover_image_url_sim: Optional[str] = None,
                                tags_sim: Optional[List[str]] = None) -> Dict[str, Any]:
        """Simulates the entire product launch process to a platform like Gumroad."""
        self._simulate_platform_delay()
        launch_id = f"launch_sim_{uuid.uuid4().hex}"
        launch_timestamp = datetime.utcnow()

        # Anti-sentience: Overall random launch failure
        if random.random() < config.SIMULATED_LAUNCH_FAIL_RATE:
            error_type = random.choice(["platform_timeout", "authentication_error_sim", "unknown_platform_error_sim"])
            logger.error(f"Simulated critical launch failure for '{vault_name}'. Type: {error_type}")
            return {
                "launch_id_sim": launch_id,
                "success": False, 
                "status": "FAILED_SIMULATED",
                "error": f"Simulated launch failure: {error_type}.",
                "timestamp_sim": launch_timestamp.isoformat() + "Z"
            }

        # 1. Simulate File Upload
        upload_result = self._simulate_file_upload(vault_file_name_sim)
        if not upload_result["success"]:
            return {
                "launch_id_sim": launch_id,
                "success": False, 
                "status": "UPLOAD_FAILED_SIMULATED",
                "error": upload_result.get("error", "Simulated file upload failed."),
                "details": upload_result,
                "timestamp_sim": launch_timestamp.isoformat() + "Z"
            }

        # 2. Simulate Product Copy/Details Submission
        # Anti-sentience: Simulate content filter for description
        simulated_copy_issue = None
        if random.random() < config.SIMULATED_COPY_FILTER_RATE:
            simulated_copy_issue = f"Simulated content policy flag on description: '{product_description_sim[:30]}...'. Requires manual review (simulated)."
            logger.warning(simulated_copy_issue)
        
        # 3. Simulate Price Setting
        if not isinstance(price_usd, (int, float)) or price_usd < 0:
            logger.error(f"Invalid price_usd provided for '{vault_name}': {price_usd}")
            return {
                "launch_id_sim": launch_id,
                "success": False, 
                "status": "INVALID_PRICE_SIMULATED",
                "error": "Invalid price provided (simulated).",
                "timestamp_sim": launch_timestamp.isoformat() + "Z"
            }

        # 4. Simulate Product Creation on Platform & Link Generation
        product_slug_sim = urllib.parse.quote_plus(vault_name.lower().replace(" ", "-"))[:50] + f"_{self._generate_simulated_short_id(4)}"
        simulated_gumroad_url = f"{config.SIMULATED_GUMROAD_BASE_URL}{product_slug_sim}"
        simulated_bitly_url = f"{config.SIMULATED_BITLY_BASE_URL}{self._generate_simulated_short_id(6)}"

        # Anti-sentience: Randomly make one of the URLs invalid or slightly off
        if random.random() < 0.03:
            if random.random() < 0.5:
                simulated_gumroad_url = f"{config.SIMULATED_GUMROAD_BASE_URL}error_slug_{self._generate_simulated_short_id(3)}"
                logger.warning("Simulated Gumroad URL generation issue.")
            else:
                simulated_bitly_url = f"{config.SIMULATED_BITLY_BASE_URL}err{self._generate_simulated_short_id(3)}"
                logger.warning("Simulated Bitly URL generation issue.")

        logger.info(f"Successfully simulated launch for '{vault_name}'.")
        return {
            "launch_id_sim": launch_id,
            "success": True,
            "status": "LAUNCHED_SUCCESSFULLY_SIMULATED",
            "vault_name": vault_name,
            "simulated_platform_product_url": simulated_gumroad_url,
            "simulated_short_link": simulated_bitly_url,
            "price_usd_sim": price_usd,
            "simulated_file_id": upload_result["file_id_sim"],
            "cover_image_url_sim_used": cover_image_url_sim,
            "tags_sim_used": tags_sim or [],
            "product_description_sim_preview": product_description_sim[:100] + "...",
            "simulated_copy_filter_status": simulated_copy_issue or "OK_SIMULATED",
            "timestamp_sim": launch_timestamp.isoformat() + "Z"
        }

# Example Usage
if __name__ == "__main__":
    logger.info("--- Running InstantProductLauncher Example ---")
    launcher = InstantProductLauncher()

    vault_details_1 = {
        "vault_name": "Ultimate Productivity Hacks Vol. 1",
        "vault_file_name_sim": "productivity_hacks_v1_final.pdf",
        "price_usd": 19.99,
        "product_description_sim": "Discover 100+ actionable productivity hacks to supercharge your workflow and reclaim your time. This vault is packed with insights!",
        "cover_image_url_sim": "https://sim.aifolio.stability.ai/v1/images/prod_cover_sim_1.png",
        "tags_sim": ["productivity", "self-help", "efficiency"]
    }

    launch_result_1 = launcher.simulate_product_launch(**vault_details_1)
    print("\n🚀 Simulated Launch Attempt 1: 🚀")
    print(json.dumps(launch_result_1, indent=2))
    print("---")

    vault_details_2 = {
        "vault_name": "AI Marketing Secrets (Limited Edition)",
        "vault_file_name_sim": "ai_marketing_secrets_le.zip",
        "price_usd": 49.00,
        "product_description_sim": "Unlock the secrets of AI in marketing. This exclusive guide reveals strategies used by top professionals. WARNING: May contain powerful ideas.",
        "cover_image_url_sim": "https://sim.aifolio.stability.ai/v1/images/ai_marketing_cover_sim.jpeg",
        "tags_sim": ["ai", "marketing", "business", "exclusive"]
    }
    
    # Run a few times to see potential random failures/issues
    for i in range(3):
        print(f"\n🚀 Simulated Launch Attempt 2 (Iteration {i+1}): 🚀")
        launch_result_2 = launcher.simulate_product_launch(**vault_details_2)
        print(json.dumps(launch_result_2, indent=2))
        print("---")

    vault_details_invalid_price = {
        "vault_name": "Test Vault Invalid Price",
        "vault_file_name_sim": "test_invalid.pdf",
        "price_usd": -5.00, # Invalid price
        "product_description_sim": "This product has an invalid price."
    }
    launch_result_invalid = launcher.simulate_product_launch(**vault_details_invalid_price)
    print("\n🚀 Simulated Launch Attempt (Invalid Price): 🚀")
    print(json.dumps(launch_result_invalid, indent=2))
    print("---")

    logger.info("--- InstantProductLauncher Example Finished ---")

