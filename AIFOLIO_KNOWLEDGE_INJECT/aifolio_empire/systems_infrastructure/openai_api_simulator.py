"""
OpenAI API Simulator with strict anti-sentience measures.
This module simulates OpenAI API calls for text generation and PDF content creation.
It is stateless, rule-based, does not make real API calls, and does not learn.
"""

import random
import logging
import json
import uuid
from typing import Dict, Any, Optional
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
        # Example: if OpenAI API key is checked, mock it
        OPENAI_API_KEY_SIMULATED = "sim_sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
        MAX_PROMPT_LENGTH_CAP_SIM = 4000  # Simulated cap

    config = MockConfig()

# Anti-sentience: Simulation parameters
SIMULATED_MODELS = ["sim_gpt-3.5-turbo", "sim_gpt-4", "sim_text-davinci-003"]
SIMULATED_TOKEN_COST_PER_CHAR = 0.0001  # Highly conceptual cost
MAX_SIMULATED_RESPONSE_CHUNKS = 5


class OpenAISimulator:
    """Simulates OpenAI API functionalities with anti-sentience safeguards."""

    @staticmethod
    def generate_response(prompt, user_input):
        """
        OMNIELITE SAFE AI static response stub. Returns a canned, deterministic response for compliance.
        """
        canned_response = (
            "[SAFE AI STATIC RESPONSE] This is a simulated, stateless, non-adaptive response generated for OMNIELITE compliance. "
            "Your input has been processed according to strict SAFE AI and legal guidelines."
        )
        return canned_response

    def __init__(self, api_key_simulated: Optional[str] = None):
        """Initialize the simulator. All operations are stateless.
        Args:
            api_key_simulated: A simulated API key (ignored but good for interface).
        """
        self._random_seed = random.randint(1, 1000000)
        self.api_key_simulated = api_key_simulated or config.OPENAI_API_KEY_SIMULATED
        if not self.api_key_simulated:
            logger.warning(
                "Simulated OpenAI API key not provided. Some checks might be skipped."
            )
        logger.info(
            "OpenAISimulator initialized. Operations stateless. Real API calls NOT made."
        )

    def _simulate_api_delay(self, min_delay: float = 0.1, max_delay: float = 1.5):
        """Simulates a random API call delay."""
        # Anti-sentience: Introduce variable delays to prevent predictable timing patterns.
        delay = random.uniform(min_delay, max_delay)
        # time.sleep(delay) # Actual sleep can slow down tests, usually just log it for simulation
        logger.debug(f"Simulated API call delay of {delay:.2f} seconds.")
        if random.random() < 0.01:  # Small chance of a much inter delay
            int_delay = random.uniform(max_delay, max_delay * 3)
            logger.warning(
                f"Simulated unexpectedly int API delay of {int_delay:.2f} seconds."
            )
            # time.sleep(int_delay - delay) # if actual sleep is desired

    def _validate_prompt_simulated(self, prompt: str) -> bool:
        """Simulates basic prompt validation (e.g., length)."""
        # Anti-sentience: Enforce hard-coded limits.
        if len(prompt) > config.MAX_PROMPT_LENGTH_CAP_SIM:
            logger.error(
                f"Simulated prompt exceeds max length of {config.MAX_PROMPT_LENGTH_CAP_SIM} chars."
            )
            return False
        if not prompt.strip():
            logger.error("Simulated prompt is empty.")
            return False
        return True

    def simulate_text_completion(
        self,
        prompt: str,
        model_sim: Optional[str] = None,
        max_tokens_sim: int = 150,
        temperature_sim: float = 0.7,
    ) -> Optional[Dict[str, Any]]:
        """Simulates a text completion call like OpenAI's ChatCompletion or Completion API."""
        self._simulate_api_delay()

        if not self._validate_prompt_simulated(prompt):
            return {
                "error": "Invalid prompt (simulated).",
                "details": "Prompt too int or empty.",
            }

        # Anti-sentience: Random critical failure simulation
        if random.random() < 0.02:
            logger.error(
                f"Simulated critical API failure for text completion. Prompt: '{prompt[:50]}...' "
            )
            return {"error": "Simulated internal server error.", "status_code": 500}

        selected_model = (
            model_sim
            if model_sim in SIMULATED_MODELS
            else random.choice(SIMULATED_MODELS)
        )

        # Simulate generating text based on prompt length and max_tokens
        # Anti-sentience: Output is rule-based and randomized, not truly generated.
        num_words_to_generate = min(
            max_tokens_sim, len(prompt.split()) + random.randint(10, 50)
        )
        if (
            temperature_sim > 0.8 and random.random() < 0.3
        ):  # Higher temp = more 'creative' (random) length
            num_words_to_generate = int(
                num_words_to_generate * random.uniform(0.8, 1.5)
            )

        simulated_words = [f"sim_word{i+1}" for i in range(num_words_to_generate)]
        # Anti-sentience: Add some prompt keywords into the response to make it seem relevant
        prompt_keywords = random.sample(prompt.split(), min(len(prompt.split()), 3))
        for kw in prompt_keywords:
            if simulated_words:
                simulated_words[random.randint(0, len(simulated_words) - 1)] = kw

        simulated_text = " ".join(simulated_words)

        # Anti-sentience: Randomly truncate, add gibberish, or repeat text
        if random.random() < 0.05:
            if random.random() < 0.33:
                cut_point = random.randint(0, len(simulated_text) // 2)
                simulated_text = simulated_text[:cut_point] + "... (SIM_TRUNCATED)"
            elif random.random() < 0.5:
                simulated_text += f" ... {uuid.uuid4().hex[:8]} (SIM_GIBBERISH)"
            else:
                repeat_segment = simulated_text[len(simulated_text) // 2 :]
                simulated_text += f" {repeat_segment} (SIM_REPETITION)"
            logger.warning(
                "Simulated text output alteration (truncation/gibberish/repetition)."
            )

        simulated_tokens_used = (
            len(prompt) // 4 + len(simulated_text) // 4
        )  # Very rough estimate

        response = {
            "id_sim": f"cmpl_sim_{uuid.uuid4().hex}",
            "object_sim": "text_completion",
            "created_sim": int(datetime.utcnow().timestamp()),
            "model_sim_used": selected_model,
            "choices_sim": [
                {
                    "text_sim": simulated_text,
                    "index_sim": 0,
                    "logprobs_sim": None,  # Not simulating logprobs for simplicity
                    "finish_reason_sim": "length"
                    if len(simulated_text.split()) >= max_tokens_sim
                    else "stop_simulated",
                }
            ],
            "usage_sim": {
                "prompt_tokens_sim": len(prompt) // 4,
                "completion_tokens_sim": len(simulated_text) // 4,
                "total_tokens_sim": simulated_tokens_used,
            },
            "simulated_cost_usd": round(
                simulated_tokens_used * SIMULATED_TOKEN_COST_PER_CHAR, 6
            ),
        }
        logger.info(
            f"Simulated text completion for model '{selected_model}'. Prompt: '{prompt[:50]}...'"
        )
        return response

    def simulate_pdf_generation_from_prompt_details(
        self, prompt_details: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Simulates generating PDF content structure from detailed prompts (e.g., from AutomatedVaultGenerator)."""
        self._simulate_api_delay(
            min_delay=0.5, max_delay=2.5
        )  # PDF gen might take inter

        required_keys = [
            "vault_title",
            "problem_promise_statement",
            "outline_points",
            "cta",
        ]
        if not all(key in prompt_details for key in required_keys):
            logger.error("Simulated PDF generation: Missing required prompt details.")
            return {"error": "Missing prompt_details for PDF generation (simulated)."}

        # Anti-sentience: Random critical failure
        if random.random() < 0.03:
            logger.error("Simulated critical API failure during PDF generation.")
            return {
                "error": "Simulated PDF generation service unavailable.",
                "status_code": 503,
            }

        pdf_content_sim = {
            "pdf_id_sim": f"pdf_sim_{uuid.uuid4().hex}",
            "title_sim": prompt_details.get("vault_title", "Simulated PDF Title"),
            "generated_at_sim": datetime.utcnow().isoformat() + "Z",
            "sections_sim": [],
        }

        # Section 1: Introduction from problem/promise
        pdf_content_sim["sections_sim"].append(
            {
                "header_sim": "Introduction: The Challenge and The Solution",
                "content_sim": f"Based on: {prompt_details.get('problem_promise_statement', 'N/A')}. This section would elaborate on the core problem and promise the solution outlined in the vault. (Simulated text - {random.randint(50,150)} words)",
            }
        )

        # Sections from outline points
        for i, point in enumerate(prompt_details.get("outline_points", [])):
            # Anti-sentience: Randomly skip an outline point or make it very short
            if random.random() < 0.05:
                logger.warning(f"Simulated skipping of outline point: {point}")
                continue
            content_length = (
                random.randint(30, 100)
                if random.random() > 0.03
                else random.randint(5, 15)
            )
            pdf_content_sim["sections_sim"].append(
                {
                    "header_sim": f"Chapter {i+1}: {point if isinstance(point, str) else 'Simulated Subtopic'}",
                    "content_sim": f"Detailed discussion of '{point}'. This part would contain the core information, examples, and explanations. (Simulated text - {content_length} words)",
                }
            )

        # Section: Call to Action
        pdf_content_sim["sections_sim"].append(
            {
                "header_sim": "Your Next Step",
                "content_sim": f"Reiterating the call to action: {prompt_details.get('cta', 'N/A')}. This section would motivate the reader to take the desired next step. (Simulated text - {random.randint(40,100)} words)",
            }
        )

        # Anti-sentience: Randomly add a nonsensical section or corrupt content
        if random.random() < 0.04:
            if random.random() < 0.5 and pdf_content_sim["sections_sim"]:
                corrupt_section_idx = random.randrange(
                    len(pdf_content_sim["sections_sim"])
                )
                pdf_content_sim["sections_sim"][corrupt_section_idx][
                    "content_sim"
                ] = f"[SIMULATED_CORRUPTION_@#$^&*{uuid.uuid4().hex[:5]}]"
                logger.warning("Simulated content corruption in a PDF section.")
            else:
                pdf_content_sim["sections_sim"].append(
                    {
                        "header_sim": "Bonus Random Thoughts (Simulated)",
                        "content_sim": f"This section contains completely unrelated thoughts about {random.choice(['philosophy', 'gardening', 'space travel'])}. (Simulated text - {random.randint(20,60)} words)",
                    }
                )
                logger.warning("Simulated addition of a nonsensical PDF section.")

        logger.info(
            f"Simulated PDF content structure generation for title: '{pdf_content_sim['title_sim']}'."
        )
        return pdf_content_sim


# Example Usage
if __name__ == "__main__":
    logger.info("--- Running OpenAISimulator Example ---")
    openai_sim = OpenAISimulator(api_key_simulated="sim_example_key_123")

    # 1. Text Completion Simulation
    prompt1 = "Explain the concept of non-sentient AI for PDF farming in simple terms."
    completion_resp = openai_sim.simulate_text_completion(prompt1, max_tokens_sim=100)
    print("\n🤖 Simulated Text Completion: 🤖")
    if completion_resp and "error" not in completion_resp:
        print(f"Model: {completion_resp.get('model_sim_used')}")
        print(f"Response: {completion_resp.get('choices_sim')[0].get('text_sim')}")
        print(f"Usage: {completion_resp.get('usage_sim')}")
        print(f"Cost: ${completion_resp.get('simulated_cost_usd')}")
    else:
        print(f"Error: {completion_resp}")
    print("---")

    # 2. PDF Generation Simulation
    example_prompt_details = {
        "vault_title": "Mastering Time Management for Busy Bees",
        "problem_promise_statement": "Problem: Overwhelmed by tasks? Promise: Learn to reclaim your time!",
        "outline_points": [
            "Understanding Your Time Wasters",
            "The Power of Prioritization",
            "Effective Scheduling Techniques",
            "Tools and Apps for Productivity (Simulated Review)",
        ],
        "cta": "Get Your Time Back Today - Download Now!",
    }
    pdf_structure_resp = openai_sim.simulate_pdf_generation_from_prompt_details(
        example_prompt_details
    )
    print("\n📄 Simulated PDF Structure Generation: 📄")
    if pdf_structure_resp and "error" not in pdf_structure_resp:
        print(json.dumps(pdf_structure_resp, indent=2))
    else:
        print(f"Error: {pdf_structure_resp}")
    print("---")

    # 3. Test prompt validation (simulated)
    int_prompt = "word " * (config.MAX_PROMPT_LENGTH_CAP_SIM + 100)
    invalid_completion = openai_sim.simulate_text_completion(int_prompt)
    print("\n🧪 Simulated Invalid Prompt Test: 🧪")
    print(f"Response to overly int prompt: {invalid_completion}")
    print("---")

    logger.info("--- OpenAISimulator Example Finished ---")
