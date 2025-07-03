"""
PDF Outline Template Simulator for Notion Ecosystem with anti-sentience measures.
This module simulates the generation of data for PDF Outline Templates in Notion.
It's stateless, rule-based, and includes randomization and simulated imperfections.
"""

import random
import logging
import uuid
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta, timezone

# Attempt to import config and logger
try:
    from config import config, logger
except ImportError:
    print("Warning: Could not import 'config' and 'logger' directly. Using basic logging.")
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    class MockConfig:
        SIM_PDF_OUTLINE_NUM_TEMPLATES_MIN = 10
        SIM_PDF_OUTLINE_NUM_TEMPLATES_MAX = 30
        SIM_PDF_OUTLINE_MAX_SECTIONS = 10
        SIM_PDF_OUTLINE_MAX_SUBSECTIONS = 3
        SIM_PDF_OUTLINE_SECTION_NOTE_CHANCE = 0.15
    config = MockConfig()

SIMULATED_TEMPLATE_CATEGORIES = [
    "How-To Guide", "Case Study Report", "Lead Magnet Blueprint", "Checklist/Cheatsheet",
    "Product Showcase_sim", "Research Paper_sim", "Tutorial Series_sim", "Ebook Starter_sim"
]
SIMULATED_SECTION_TITLES = [
    "Introduction", "The Problem We Solve", "Understanding {Topic}", "Key Benefits", "Core Concepts",
    "Step-by-Step Guide", "Chapter {N}: {Detail}", "Advanced Techniques", "Common Mistakes to Avoid",
    "Case Study: {Example}", "Tools and Resources", "Conclusion & Next Steps", "FAQ_sim", "Glossary_sim"
]
SIMULATED_SECTION_PLACEHOLDER_CONTENT = [
    "[Placeholder: Briefly introduce the topic and its importance. Simulated text.]",
    "[Placeholder: Detail the main challenge or pain point this section addresses. Simulated content.]",
    "[Placeholder: Explain the core ideas or steps related to this section. Use bullet points for clarity if needed. Simulated.]",
    "[Placeholder: Summarize key takeaways for this section. What should the reader remember? Simulated.]",
    "[Placeholder: Add supporting data, examples, or visuals descriptions here. Simulated.]"
]
SIMULATED_TEMPLATE_TAGS = [
    "beginner-friendly", "expert-level", "marketing_pdf", "educational_pdf", "sales_tool",
    "quick_reference", "in-depth_analysis", "problem_solution", "value_proposition_sim"
]

class PDFOutlineTemplateSimulator:
    """Simulates data for Notion PDF Outline Templates with anti-sentience safeguards."""

    def __init__(self):
        """Initialize the simulator. Operations are stateless per call."""
        self._random_seed = random.randint(1, 1000000)
        logger.info("PDFOutlineTemplateSimulator initialized. Operations stateless.")

    def _generate_simulated_sections(self, max_depth: int, current_depth: int = 0, topic_sim: str = "Generic Topic") -> List[Dict[str, Any]]:
        if current_depth >= max_depth:
            return []
        logger.info(f"Generating simulated PDF outline sections at depth {current_depth} for topic '{topic_sim}'")
        num_sections = random.randint(1, config.SIM_PDF_OUTLINE_MAX_SECTIONS - current_depth * 2) # Fewer sections deeper
        sections = []
        for i in range(num_sections):
            title_template = random.choice(SIMULATED_SECTION_TITLES)
            # Basic placeholder replacement for simulated dynamic titles
            section_title = title_template.replace("{Topic}", topic_sim)\
                                        .replace("{N}", str(i + 1))\
                                        .replace("{Detail}", f"Detail Part {chr(65+i)}")\
                                        .replace("{Example}", f"Example {i+1}")
            
            section_note = None
            if random.random() < config.SIM_PDF_OUTLINE_SECTION_NOTE_CHANCE:
                section_note = f"Simulated Note: Consider adding a visual or example for '{section_title}'."

            section = {
                "section_id_sim": f"sec_{uuid.uuid4().hex[:8]}",
                "section_title_sim": section_title,
                "content_placeholder_sim": random.choice(SIMULATED_SECTION_PLACEHOLDER_CONTENT),
                "estimated_pages_sim": random.randint(1,3) if current_depth < 2 else 1, # Sub-sections are shorter
                "note_sim": section_note,
                "sub_sections_sim": []
            }
            if current_depth < max_depth -1: # Only add subsections if not at max depth for subsections
                 if random.random() < 0.3 / (current_depth + 1): # Higher chance for subsections at shallower depths
                    section["sub_sections_sim"] = self._generate_simulated_sections(max_depth, current_depth + 1, topic_sim)
            sections.append(section)
        return sections

    def get_simulated_outline_templates(self, num_templates: Optional[int] = None) -> Dict[str, Any]:
        """Generates a list of simulated PDF outline templates.
        Args:
            num_templates: Optional. Number of templates to simulate. 
                           If None, uses config min/max.
        Returns:
            A dictionary containing the list of simulated template entries and metadata.
        """
        action_id = f"pdf_outline_templates_{uuid.uuid4().hex[:8]}"
        template_entries = []
        
        if num_templates is None:
            num_to_simulate = random.randint(config.SIM_PDF_OUTLINE_NUM_TEMPLATES_MIN, 
                                             config.SIM_PDF_OUTLINE_NUM_TEMPLATES_MAX)
        else:
            num_to_simulate = max(0, num_templates)

        current_time = datetime.now(timezone.utc)

        for i in range(num_to_simulate):
            category = random.choice(SIMULATED_TEMPLATE_CATEGORIES)
            sim_topic = f"Simulated Topic {chr(65+i % 26)}{i//26 if i//26 > 0 else ''}"
            name = f"{category} Template for {sim_topic} - Var {random.randint(1,100)}"
            description = f"A simulated PDF outline template for creating a {category.lower()} on {sim_topic}. Contains placeholder sections and content suggestions."
            
            num_tags = random.randint(1, 3)
            tags = random.sample(SIMULATED_TEMPLATE_TAGS, num_tags)
            
            # Max depth for sections/subsections (e.g., 2 means sections and one level of sub-sections)
            max_nesting_depth = random.randint(1, config.SIM_PDF_OUTLINE_MAX_SUBSECTIONS + 1)
            sections = self._generate_simulated_sections(max_depth=max_nesting_depth, topic_sim=sim_topic)

            entry = {
                "template_id_sim": f"tpl_{uuid.uuid4().hex[:10]}",
                "template_name_sim": name,
                "description_sim": description,
                "category_sim": category,
                "sections_sim": sections,
                "tags_sim": tags,
                "complexity_sim": random.choice(["Basic", "Intermediate", "Advanced_sim"]), 
                "created_at_sim": (current_time - timedelta(days=random.randint(30, 400))).isoformat(),
                "last_updated_sim": (current_time - timedelta(days=random.randint(0, 29))).isoformat(),
                "author_sim": "AIFOLIO Simulator"
            }
            template_entries.append(entry)
        
        template_entries.sort(key=lambda x: x["category_sim"] + x["template_name_sim"])

        return {
            "action_id_sim": action_id,
            "generated_at_utc_sim": current_time.isoformat(),
            "pdf_outline_templates_sim": template_entries,
            "data_source_sim": "AIFOLIO Empire Mode - PDF Outline Template Simulator",
            "anti_sentience_notes": [
                "All outline templates, including structure and content, are randomly generated and simulated.",
                "Section titles and placeholder text are for structural demonstration only.",
                f"Simulated notes or advice within templates are intentional ({config.SIM_PDF_OUTLINE_SECTION_NOTE_CHANCE*100}% chance per section)."
            ]
        }

# Example Usage:
if __name__ == "__main__":
    import json
    logger.info("--- Running PDFOutlineTemplateSimulator Example ---")
    simulator = PDFOutlineTemplateSimulator()

    print("\n📑 Simulated PDF Outline Templates (Default Number): 📑")
    template_data = simulator.get_simulated_outline_templates()
    print(json.dumps(template_data, indent=2, ensure_ascii=False))
    print(f"Generated {len(template_data['pdf_outline_templates_sim'])} template entries.")

    print("\n📑 Simulated PDF Outline Templates (Specific Number: 2): 📑")
    template_data_specific = simulator.get_simulated_outline_templates(num_templates=2)
    # Pretty print one entry to see structure
    if template_data_specific['pdf_outline_templates_sim']:
        print("\nExample of one template structure:")
        print(json.dumps(template_data_specific['pdf_outline_templates_sim'][0], indent=2, ensure_ascii=False))
    print(f"Generated {len(template_data_specific['pdf_outline_templates_sim'])} template entries.")

    logger.info("--- PDFOutlineTemplateSimulator Example Finished ---")

