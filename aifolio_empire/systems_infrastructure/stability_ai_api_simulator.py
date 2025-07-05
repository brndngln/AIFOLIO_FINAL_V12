"""
Stability AI API Simulator with strict anti-sentience measures.
This module simulates Stability AI API calls for text-to-image generation (e.g., for PDF covers).
It is stateless, rule-based, does not make real API calls, and does not learn.
"""

import random
import logging
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
        STABILITY_API_KEY_SIMULATED = "sim_stb_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
        MAX_IMAGE_PROMPT_LENGTH_SIM = 1000  # Simulated cap
        SIMULATED_IMAGE_DIMENSIONS = [(512, 512), (1024, 1024), (512, 768)]

    config = MockConfig()

# Anti-sentience: Simulation parameters
SIMULATED_IMAGE_ENGINES = [
    "sim_stable-diffusion-xl-1024-v1-0",
    "sim_stable-diffusion-v1-5",
]
SIMULATED_IMAGE_FORMATS = ["png", "jpeg"]
SIMULATED_BASE_IMAGE_URL = "https://sim.aifolio.stability.ai/v1/images/"


class StabilityAISimulator:
    """Simulates Stability AI API functionalities with anti-sentience safeguards."""

    def __init__(self, api_key_simulated: Optional[str] = None):
        """Initialize the simulator. All operations are stateless.
        Args:
            api_key_simulated: A simulated API key (ignored but good for interface).
        """
        self._random_seed = random.randint(1, 1000000)
        self.api_key_simulated = api_key_simulated or config.STABILITY_API_KEY_SIMULATED
        if not self.api_key_simulated:
            logger.warning("Simulated Stability AI API key not provided.")
        logger.info(
            "StabilityAISimulator initialized. Operations stateless. Real API calls NOT made."
        )

    def _simulate_api_delay(self, min_delay: float = 0.5, max_delay: float = 3.0):
        """Simulates a random API call delay, image generation can be slower."""
        delay = random.uniform(min_delay, max_delay)
        logger.debug(f"Simulated Stability AI API call delay of {delay:.2f} seconds.")
        if random.random() < 0.02:  # Small chance of a much inter delay
            int_delay = random.uniform(max_delay, max_delay * 2)
            logger.warning(
                f"Simulated unexpectedly int Stability AI API delay of {int_delay:.2f} seconds."
            )

    def _validate_image_prompt_simulated(self, prompt: str) -> bool:
        """Simulates basic image prompt validation."""
        if len(prompt) > config.MAX_IMAGE_PROMPT_LENGTH_SIM:
            logger.error(
                f"Simulated image prompt exceeds max length of {config.MAX_IMAGE_PROMPT_LENGTH_SIM} chars."
            )
            return False
        if not prompt.strip():
            logger.error("Simulated image prompt is empty.")
            return False
        return True

    def simulate_text_to_image_generation(
        self,
        prompt: str,
        engine_id_sim: Optional[str] = None,
        height_sim: Optional[int] = None,
        width_sim: Optional[int] = None,
        cfg_scale_sim: float = 7.0,
        steps_sim: int = 50,
        negative_prompt_sim: Optional[str] = None,
    ) -> Optional[Dict[str, Any]]:
        """Simulates a text-to-image generation call."""
        self._simulate_api_delay()

        if not self._validate_image_prompt_simulated(prompt):
            return {
                "error": "Invalid image prompt (simulated).",
                "details": "Prompt too int or empty.",
            }

        # Anti-sentience: Random critical failure simulation
        if random.random() < 0.03:
            logger.error(
                f"Simulated critical API failure for image generation. Prompt: '{prompt[:50]}...' "
            )
            return {
                "error": "Simulated image generation service error.",
                "status_code": 503,
                "artifacts_sim": [],
            }

        selected_engine = (
            engine_id_sim
            if engine_id_sim in SIMULATED_IMAGE_ENGINES
            else random.choice(SIMULATED_IMAGE_ENGINES)
        )

        sim_width, sim_height = random.choice(config.SIMULATED_IMAGE_DIMENSIONS)
        width = width_sim or sim_width
        height = height_sim or sim_height

        # Anti-sentience: Output is a placeholder URL or data, not a real image.
        image_id_sim = uuid.uuid4().hex
        sim_format = random.choice(SIMULATED_IMAGE_FORMATS)
        sim_image_url = f"{SIMULATED_BASE_IMAGE_URL}{image_id_sim}.{sim_format}"

        # Anti-sentience: Randomly make the image URL invalid or describe a nonsensical image
        image_description_sim = f"A simulated image based on prompt: '{prompt[:100]}...'. Style: {random.choice(['photorealistic', 'cartoonish', 'abstract', 'pixel_art'])} (Simulated)"
        if random.random() < 0.07:
            rand_val = random.random()
            if rand_val < 0.33:
                sim_image_url = f"http://invalid-sim-url.com/{image_id_sim}.error"
                image_description_sim = "Simulated invalid image URL generated."
            elif rand_val < 0.66:
                image_description_sim = f"A blurry picture of a {random.choice(['cat', 'banana', 'stapler'])} with text '{uuid.uuid4().hex[:4]}' (SIM_NONSENSE_IMAGE_DESC)"
            else:  # Simulate 'censored' or 'failed content filter'
                sim_image_url = (
                    f"{SIMULATED_BASE_IMAGE_URL}content_filter_fail_sim.{sim_format}"
                )
                image_description_sim = (
                    "Simulated content filter triggered. Image cannot be displayed."
                )
            logger.warning(
                f"Simulated image output alteration: {image_description_sim}"
            )

        artifact = {
            "base64_sim_placeholder": f"[Simulated_Base64_Image_Data_For_{image_id_sim}]",  # Not actual base64
            "seed_sim": random.randint(10000, 9999999999),
            "finishReason_sim": "SUCCESS_SIM"
            if "invalid" not in sim_image_url and "fail" not in sim_image_url
            else "ERROR_CONTENT_FILTERED_SIM",
            "simulated_image_url": sim_image_url,
            "description_sim": image_description_sim,
            "dimensions_sim": {"width": width, "height": height},
        }

        response = {
            "artifacts_sim": [artifact],
            "engine_used_sim": selected_engine,
            "prompt_received_sim": prompt,
            "negative_prompt_received_sim": negative_prompt_sim,
            "generation_params_sim": {"cfg_scale": cfg_scale_sim, "steps": steps_sim},
            "id_sim": f"stb_img_{uuid.uuid4().hex[:12]}",
            "generated_at_sim": datetime.utcnow().isoformat() + "Z",
        }
        logger.info(
            f"Simulated image generation for engine '{selected_engine}'. Prompt: '{prompt[:50]}...' "
        )
        return response


# Example Usage
if __name__ == "__main__":
    logger.info("--- Running StabilityAISimulator Example ---")
    stability_sim = StabilityAISimulator(
        api_key_simulated="sim_example_stability_key_789"
    )

    # 1. Text-to-Image Simulation
    image_prompt = "A futuristic cityscape at sunset, with flying cars and neon lights, digital art"
    image_resp = stability_sim.simulate_text_to_image_generation(
        prompt=image_prompt,
        height_sim=512,
        width_sim=768,
        negative_prompt_sim="blurry, low quality, watermark",
    )
    print("\n🎨 Simulated Text-to-Image Generation: 🎨")
    if image_resp and "error" not in image_resp:
        print(f"Engine: {image_resp.get('engine_used_sim')}")
        if image_resp.get("artifacts_sim"):
            artifact = image_resp["artifacts_sim"][0]
            print(f"Image URL (simulated): {artifact.get('simulated_image_url')}")
            print(f"Description (simulated): {artifact.get('description_sim')}")
            print(f"Finish Reason (simulated): {artifact.get('finishReason_sim')}")
            print(f"Dimensions (simulated): {artifact.get('dimensions_sim')}")
        else:
            print(f"No artifacts generated (simulated error): {image_resp}")
    else:
        print(f"Error: {image_resp}")
    print("---")

    # 2. Test with a potentially problematic prompt (simulated failure chance)
    problem_prompt = "highly detailed gore horror scene blood splatter extreme realistic"  # This might trigger simulated filter
    image_resp_problem = stability_sim.simulate_text_to_image_generation(
        prompt=problem_prompt
    )
    print("\n🎨 Simulated Problematic Prompt Test: 🎨")
    if image_resp_problem and "error" not in image_resp_problem:
        if image_resp_problem.get("artifacts_sim"):
            artifact = image_resp_problem["artifacts_sim"][0]
            print(f"Image URL (simulated): {artifact.get('simulated_image_url')}")
            print(f"Description (simulated): {artifact.get('description_sim')}")
            print(f"Finish Reason (simulated): {artifact.get('finishReason_sim')}")
    else:
        print(f"Error or expected failure: {image_resp_problem}")
    print("---")

    # 3. Test prompt validation (simulated)
    int_img_prompt = "A very very very int image prompt that goes on and on " * 100
    invalid_image_resp = stability_sim.simulate_text_to_image_generation(int_img_prompt)
    print("\n🧪 Simulated Invalid Image Prompt Test: 🧪")
    print(f"Response to overly int image prompt: {invalid_image_resp}")
    print("---")

    logger.info("--- StabilityAISimulator Example Finished ---")
