"""
Prompt Library Data Simulator for Notion Ecosystem with anti-sentience measures.
This module simulates the generation of data for a Prompt Library in Notion.
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
        SIM_PROMPT_LIB_NUM_PROMPTS_MIN = 15
        SIM_PROMPT_LIB_NUM_PROMPTS_MAX = 50
        SIM_PROMPT_LIB_MAX_USAGE_COUNT = 1000
        SIM_PROMPT_LIB_RATING_GLITCH_CHANCE = 0.05 # Chance of an unusual rating
        SIM_PROMPT_LIB_TEXT_PLACEHOLDER_NOTE_CHANCE = 0.1 # Chance to add a note about placeholder text
    config = MockConfig()

SIMULATED_PROMPT_CATEGORIES = [
    "PDF Outline Generation", "Sales Page Copywriting", "Email Sequence Crafting",
    "Social Media Posts", "Blog Post Ideas", "Product Descriptions_sim",
    "Vault Title Brainstorming", "Image Generation Concepts_sim", "Ad Copy_sim", "Video Script Ideas_sim"
]
SIMULATED_PROMPT_TAGS = [
    "beginner", "advanced", "marketing", "content_creation", "sales_funnel", "engagement",
    "conversion", "storytelling", "technical_sim", "creative_sim", "short_form", "long_form"
]
SIMULATED_PROMPT_TEMPLATES = [
    ("Generate a {length} {type} for a product about {topic}", ["length", "type", "topic"]),
    ("Create 5 compelling {hook_type} hooks for a {platform} post on {niche}", ["hook_type", "platform", "niche"]),
    ("Write a persuasive {email_type} email to encourage sign-ups for a {offering}", ["email_type", "offering"]),
    ("Outline a 7-section PDF vault titled '{vault_title_core}' focusing on {key_benefit}", ["vault_title_core", "key_benefit"]),
    ("Suggest 3 creative concepts for a cover image for a vault about {subject_matter}", ["subject_matter"])
]

class PromptLibraryDataSimulator:
    """Simulates data generation for a Notion Prompt Library with anti-sentience safeguards."""

    def __init__(self):
        """Initialize the simulator. Operations are stateless per call."""
        self._random_seed = random.randint(1, 1000000)
        logger.info("PromptLibraryDataSimulator initialized. Operations stateless.")

    def _generate_simulated_prompt_text(self) -> Dict[str, Any]:
        template, placeholders = random.choice(SIMULATED_PROMPT_TEMPLATES)
        filled_template = template
        sim_params = {}
        for p_holder in placeholders:
            sim_value = f"<SIMULATED_{p_holder.upper()}>"
            filled_template = filled_template.replace(f"{{{p_holder}}}", sim_value)
            sim_params[p_holder] = sim_value
        
        notes = None
        if random.random() < config.SIM_PROMPT_LIB_TEXT_PLACEHOLDER_NOTE_CHANCE:
            notes = "Note: This prompt text is a basic template. Actual usage requires replacing placeholders with specific details (simulated)."
        
        return {"text": filled_template, "simulated_params": sim_params, "notes_sim": notes}

    def get_simulated_prompt_library_data(self, num_prompts: Optional[int] = None) -> Dict[str, Any]:
        """Generates a list of simulated prompt entries for the library.
        Args:
            num_prompts: Optional. Number of prompts to simulate. 
                         If None, uses config min/max.
        Returns:
            A dictionary containing the list of simulated prompt entries and metadata.
        """
        action_id = f"prompt_lib_data_{uuid.uuid4().hex[:8]}"
        prompt_entries = []
        
        if num_prompts is None:
            num_to_simulate = random.randint(config.SIM_PROMPT_LIB_NUM_PROMPTS_MIN, 
                                             config.SIM_PROMPT_LIB_NUM_PROMPTS_MAX)
        else:
            num_to_simulate = max(0, num_prompts)

        current_time = datetime.now(timezone.utc)

        for i in range(num_to_simulate):
            category = random.choice(SIMULATED_PROMPT_CATEGORIES)
            prompt_gen_result = self._generate_simulated_prompt_text()
            prompt_text = prompt_gen_result["text"]
            sim_params = prompt_gen_result["simulated_params"]
            prompt_notes = prompt_gen_result["notes_sim"]

            name = f"Simulated Prompt for {category} - Var {random.randint(100,999)}"
            num_tags = random.randint(1, 3)
            tags = random.sample(SIMULATED_PROMPT_TAGS, num_tags)
            
            rating = round(random.uniform(2.5, 5.0), 1)
            if random.random() < config.SIM_PROMPT_LIB_RATING_GLITCH_CHANCE:
                rating = random.choice([round(random.uniform(0.5, 2.0),1), None]) # Simulate a bad or missing rating
                if prompt_notes:
                    prompt_notes += " Rating may be unreliable (simulated glitch)."
                else:
                    prompt_notes = "Rating may be unreliable (simulated glitch)."

            entry = {
                "prompt_id_sim": f"prompt_{uuid.uuid4().hex[:10]}",
                "prompt_name_sim": name,
                "prompt_text_sim": prompt_text,
                "simulated_parameters": sim_params,
                "category_sim": category,
                "tags_sim": tags,
                "usage_count_sim": random.randint(0, config.SIM_PROMPT_LIB_MAX_USAGE_COUNT),
                "rating_sim": rating, # Scale of 1-5, or None
                "created_at_sim": (current_time - timedelta(days=random.randint(10, 365))).isoformat(),
                "last_updated_sim": (current_time - timedelta(days=random.randint(0, 9))).isoformat(),
                "source_sim": "AIFOLIO Simulated Library",
                "notes_sim": prompt_notes
            }
            prompt_entries.append(entry)
        
        prompt_entries.sort(key=lambda x: x["category_sim"] + x["prompt_name_sim"])

        return {
            "action_id_sim": action_id,
            "generated_at_utc_sim": current_time.isoformat(),
            "prompt_library_entries_sim": prompt_entries,
            "data_source_sim": "AIFOLIO Empire Mode - Prompt Library Simulator",
            "anti_sentience_notes": [
                "All prompt data, including text and metrics, is randomly generated and simulated.",
                "Prompts are placeholders and not designed for actual AI use without significant modification.",
                f"Simulated data glitches (e.g., in ratings: {config.SIM_PROMPT_LIB_RATING_GLITCH_CHANCE*100}%) are intentional."
            ]
        }

# Example Usage:
if __name__ == "__main__":
    import json
    logger.info("--- Running PromptLibraryDataSimulator Example ---")
    simulator = PromptLibraryDataSimulator()

    print("\n📚 Simulated Prompt Library Data (Default Number): 📚")
    library_data = simulator.get_simulated_prompt_library_data()
    print(json.dumps(library_data, indent=2))
    print(f"Generated {len(library_data['prompt_library_entries_sim'])} prompt entries.")

    print("\n📚 Simulated Prompt Library Data (Specific Number: 3): 📚")
    library_data_specific = simulator.get_simulated_prompt_library_data(num_prompts=3)
    print(json.dumps(library_data_specific, indent=2))
    print(f"Generated {len(library_data_specific['prompt_library_entries_sim'])} prompt entries.")

    logger.info("--- PromptLibraryDataSimulator Example Finished ---")

