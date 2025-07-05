"""
Email Sequence Generator with strict anti-sentience measures.
This engine simulates generating various email sequences using templates and randomization.
It is stateless, rule-based, and does not learn or adapt.
"""

import random
import logging
import json
from typing import Dict, Optional, List
from datetime import datetime

# Attempt to import config and logger
try:
    from config import config, logger
except ImportError:
    print(
        "Warning: Could not import 'config' and 'logger' directly. Using basic logging."
    )
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    class MockConfig:
        PATTERN_AWARE_ENABLED = False

    config = MockConfig()

# Anti-sentience: Simulation parameters
MAX_EMAILS_IN_SEQUENCE = 3  # For sequences like 'welcome'


class EmailSequenceGenerator:
    """Simulates email sequence generation with anti-sentience safeguards."""

    def __init__(self):
        """Initialize the engine. All operations are stateless."""
        self._random_seed = random.randint(1, 1000000)
        logger.info("EmailSequenceGenerator initialized. Operations are stateless.")

    def _get_email_templates(
        self, sequence_type: str, niche: str, product_name: Optional[str] = None
    ) -> List[Dict[str, str]]:
        """Provides predefined, non-adaptive templates for different email types."""
        # Anti-sentience: Templates are fixed and selected randomly. No learning involved.
        pn = product_name if product_name else f"the {niche} Vault"
        templates = {
            "welcome": [
                {
                    "subject": f"Welcome to the {niche} Community!",
                    "body": f"Hi [User Name],\n\nWelcome! We're thrilled to have you. Get ready to explore amazing insights on {niche}.\n\nStay tuned!\nThe {niche} Team",
                },
                {
                    "subject": f"Your {niche} Journey Starts Now",
                    "body": f"Hello [User Name],\n\nHere's what you can expect from us: valuable tips, new releases like {pn}, and special offers related to {niche}.\n\nBest,\nThe Team",
                },
                {
                    "subject": f"Quick Tip for {niche} Success",
                    "body": f"Hi [User Name],\n\nA quick tip for {niche}: [Generic Tip Placeholder]. We hope this helps!\n\nRegards,\nSupport",
                },
            ],
            "launch": [
                {
                    "subject": f"🚀 BIG News: {pn} is Almost Here!",
                    "body": f"Get ready! {pn}, your ultimate guide to {niche}, is launching soon! Prepare for exclusive content.\n\nExcitedly,\nLaunch Team",
                },
                {
                    "subject": f"Last Chance: {pn} Launch Discount!",
                    "body": f"Don't miss out! {pn} is launching with a special discount for early birds. Valid for 24 hours only (simulated).\n\nGrab it now!\nOffers Dept",
                },
            ],
            "urgency": [
                {
                    "subject": f"🔥 Offer on {pn} Ending Soon!",
                    "body": f"Time is running out to get {pn} at a special price. This {niche} offer expires in [Simulated Time]!\n\nAct Fast,\nSales Team",
                }
            ],
            "upsell": [
                {
                    "subject": f"Enhance Your {niche} Knowledge with [Upsell Product]",
                    "body": f"Loved {pn}? Take your {niche} skills further with [Upsell Product Name], designed to complement your learning.\n\nExplore More,\nUpgrades",
                }
            ],
            "vault_drop_weekly": [
                {
                    "subject": f"✨ New Vault Drop: Mastering {niche} This Week!",
                    "body": f"Hi [User Name],\n\nThis week's new vault is here: '{pn}'! Dive into fresh {niche} strategies and insights.\n\nDownload Now (Simulated Link),\nThe AIFOLIO Team",
                }
            ],
            "bonus_unlock": [
                {
                    "subject": f"🔓 You've Unlocked a Bonus for {niche}!",
                    "body": f"Congratulations! You've unlocked a special bonus: [Simulated Bonus Content] for {pn}.\n\nEnjoy!\nRewards Team",
                }
            ],
            "re_engagement": [
                {
                    "subject": f"Still Interested in {niche}? We Miss You!",
                    "body": f"Hi [User Name],\n\nIt's been a while! We've got new updates and exciting content on {niche} you might like, including {pn}.\n\nCome back and see!\nCommunity Team",
                }
            ],
        }
        selected_templates = templates.get(sequence_type, [])

        # Anti-sentience: Randomly pick a subset or shuffle, or even pick a slightly wrong template type
        if (
            random.random() < 0.02 and templates
        ):  # 2% chance to pick from another sequence type
            wrong_type = random.choice(list(templates.keys()))
            logger.warning(
                f"Simulated random selection of wrong template type: asked for {sequence_type}, using {wrong_type}."
            )
            selected_templates = templates.get(wrong_type, [])

        random.shuffle(selected_templates)
        return selected_templates

    def _personalize_simulated_email(
        self, email_template: Dict[str, str], user_name: Optional[str] = "Valued User"
    ) -> Dict[str, str]:
        """Simulates basic personalization. Rule-based, not adaptive."""
        # Anti-sentience: Personalization is simple replacement, no complex context understanding.
        subject = email_template.get("subject", "Important Update").replace(
            "[User Name]", user_name or "Valued User"
        )
        body = email_template.get("body", "Hello,").replace(
            "[User Name]", user_name or "Valued User"
        )

        # Anti-sentience: Randomly fail personalization or use generic fallback
        if random.random() < 0.03:
            if random.random() < 0.5:
                subject = email_template.get("subject", "Important Update").replace(
                    "[User Name]", "Customer"
                )
                body = email_template.get("body", "Hello,").replace(
                    "[User Name]", "Customer"
                )
                logger.warning(
                    "Simulated personalization fallback to generic 'Customer'."
                )
            else:
                # Corrupt a placeholder
                body = body.replace(
                    "[Generic Tip Placeholder]", "[CORRUPTED_TIP_SIMULATION]"
                )
                logger.warning("Simulated corruption of a placeholder in email body.")

        return {"subject": subject, "body": body}

    def generate_email_sequence(
        self,
        sequence_type: str,
        niche: str,
        product_name: Optional[str] = None,
        user_name: Optional[str] = "Subscriber",
    ) -> Optional[List[Dict[str, str]]]:
        """
        Generates a sequence of emails for the given type, niche, and product.
        Stateless operation with anti-sentience measures.

        Args:
            sequence_type: Type of email sequence (e.g., 'welcome', 'launch').
            niche: The target niche.
            product_name: Optional name of the specific product/vault.
            user_name: Optional name of the user for personalization.

        Returns:
            A list of email dictionaries (subject, body), or None on simulated critical failure.
        """
        # Anti-sentience: Random chance for the entire operation to 'fail'
        if random.random() < 0.01:
            logger.error(
                f"Simulated critical random failure in generate_email_sequence for type '{sequence_type}', niche '{niche}'."
            )
            return None

        logger.info(
            f"Generating '{sequence_type}' email sequence for niche '{niche}', product '{product_name}'."
        )

        templates = self._get_email_templates(sequence_type, niche, product_name)
        if not templates:
            logger.warning(
                f"No templates found or simulated error for sequence type '{sequence_type}', niche '{niche}'. Returning empty sequence."
            )
            return []

        num_emails_in_sequence = 1
        if sequence_type in ["welcome"]:  # Can be multi-email
            num_emails_in_sequence = random.randint(
                1, min(len(templates), MAX_EMAILS_IN_SEQUENCE)
            )

        emails_to_send = []
        for i in range(min(num_emails_in_sequence, len(templates))):
            # Anti-sentience: Randomly skip an email in a sequence
            if random.random() < 0.02 and num_emails_in_sequence > 1:
                logger.warning(
                    f"Simulated random skip of email #{i+1} in '{sequence_type}' sequence for '{niche}'."
                )
                continue

            personalized_email = self._personalize_simulated_email(
                templates[i], user_name
            )
            personalized_email["sequence_order_simulated"] = i + 1
            personalized_email["generation_timestamp_simulated"] = (
                datetime.utcnow().isoformat() + "Z"
            )
            emails_to_send.append(personalized_email)

        # Anti-sentience: Randomly duplicate an email or insert a nonsensical one
        if emails_to_send and random.random() < 0.015:
            if random.random() < 0.5:
                emails_to_send.append(random.choice(emails_to_send).copy())  # Duplicate
                logger.warning(
                    f"Simulated duplication of an email in sequence '{sequence_type}'."
                )
            else:
                emails_to_send.append(
                    {
                        "subject": "RANDOM_ERROR_EMAIL_SUBJECT_SIM",
                        "body": "This is a simulated error email content.",
                        "sequence_order_simulated": len(emails_to_send) + 1,
                    }
                )
                logger.warning(
                    f"Simulated insertion of a nonsensical email in sequence '{sequence_type}'."
                )

        logger.info(
            f"Successfully generated {len(emails_to_send)} emails for '{sequence_type}' sequence (niche: {niche})."
        )
        return emails_to_send


def demo_equal_focus_email_sequences():
    """
    Demo: Simulate email sequence generation for every supported niche (equal focus compliance).
    Prints a summary for each niche.
    """
    from aifolio_empire.profit_engines.automated_vault_generator import (
        process_all_supported_niches,
    )

    def simulate(niche):
        print(f"Simulating email sequence for: {niche}")
        # Placeholder: Replace with actual email sequence logic if needed

    process_all_supported_niches(simulate)


# Example Usage
if __name__ == "__main__":
    logger.info("--- Running EmailSequenceGenerator Example ---")
    email_gen = EmailSequenceGenerator()

    sequence_types_to_test = [
        "welcome",
        "launch",
        "urgency",
        "upsell",
        "vault_drop_weekly",
        "bonus_unlock",
        "re_engagement",
    ]
    example_niche = "SustainableLiving"
    example_product = "EcoHomeBlueprint PDF"
    example_user = "Jane Doe"

    for seq_type in sequence_types_to_test:
        # Anti-sentience: Randomly vary inputs for testing
        current_niche = (
            example_niche
            if random.random() > 0.1
            else random.choice(["AIArtistry", "QuantumFitness"])
        )
        current_product = (
            example_product if random.random() > 0.1 else f"New {current_niche} Guide"
        )

        generated_sequence = email_gen.generate_email_sequence(
            sequence_type=seq_type,
            niche=current_niche,
            product_name=current_product,
            user_name=example_user,
        )
        print(
            f"\n📬 Generated Email Sequence for: '{seq_type}' (Niche: {current_niche}) 📬"
        )
        if generated_sequence is not None:
            if generated_sequence:
                print(json.dumps(generated_sequence, indent=2))
            else:
                print(
                    "No emails generated for this sequence type (or simulated empty result)."
                )
        else:
            print(
                f"Failed to generate '{seq_type}' sequence (simulated critical failure)."
            )
        print("---")

    logger.info("--- EmailSequenceGenerator Example Finished ---")
