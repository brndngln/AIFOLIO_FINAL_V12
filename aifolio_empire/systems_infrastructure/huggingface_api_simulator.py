"""
Hugging Face API Simulator with strict anti-sentience measures.
This module simulates Hugging Face Inference API calls for tasks like
summarization and sentiment analysis. It is stateless, rule-based,
does not make real API calls, and does not learn.
"""

import random
import logging
import json
import uuid
from typing import Dict, Any, Optional, List, Union
from datetime import datetime
import time

# Attempt to import config and logger
try:
    from config import config, logger
except ImportError:
    print("Warning: Could not import 'config' and 'logger' directly. Using basic logging.")
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    class MockConfig:
        HF_API_TOKEN_SIMULATED = "sim_hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
        MAX_INPUT_TEXT_LENGTH_SIM = 5000 # Simulated cap for HF models
    config = MockConfig()

# Anti-sentience: Simulation parameters
SIMULATED_HF_SUMMARIZATION_MODELS = ["sim_facebook/bart-large-cnn", "sim_google/pegasus-xsum", "sim_t5-base"]
SIMULATED_HF_SENTIMENT_MODELS = ["sim_distilbert-base-uncased-finetuned-sst-2-english", "sim_nlptown/bert-base-multilingual-uncased-sentiment"]
SIMULATED_SENTIMENT_LABELS = ["POSITIVE", "NEGATIVE", "NEUTRAL"]

class HuggingFaceSimulator:
    """Simulates Hugging Face Inference API functionalities with anti-sentience safeguards."""

    def __init__(self, api_token_simulated: Optional[str] = None):
        """Initialize the simulator. All operations are stateless.
        Args:
            api_token_simulated: A simulated API token (ignored but good for interface).
        """
        self._random_seed = random.randint(1, 1000000)
        self.api_token_simulated = api_token_simulated or config.HF_API_TOKEN_SIMULATED
        if not self.api_token_simulated:
            logger.warning("Simulated Hugging Face API token not provided.")
        logger.info("HuggingFaceSimulator initialized. Operations stateless. Real API calls NOT made.")

    def _simulate_api_delay(self, min_delay: float = 0.2, max_delay: float = 1.8):
        """Simulates a random API call delay."""
        delay = random.uniform(min_delay, max_delay)
        logger.debug(f"Simulated HF API call delay of {delay:.2f} seconds.")
        if random.random() < 0.015: # Small chance of a much longer delay
            long_delay = random.uniform(max_delay, max_delay * 2.5)
            logger.warning(f"Simulated unexpectedly long HF API delay of {long_delay:.2f} seconds.")

    def _validate_input_text_simulated(self, text: str) -> bool:
        """Simulates basic input text validation."""
        if len(text) > config.MAX_INPUT_TEXT_LENGTH_SIM:
            logger.error(f"Simulated input text exceeds max length of {config.MAX_INPUT_TEXT_LENGTH_SIM} chars.")
            return False
        if not text.strip():
            logger.error("Simulated input text is empty.")
            return False
        return True

    def simulate_summarization(self, 
                               text_to_summarize: str, 
                               model_id_sim: Optional[str] = None, 
                               min_length_sim: int = 30,
                               max_length_sim: int = 150) -> Optional[Dict[str, Any]]:
        """Simulates a text summarization call."""
        self._simulate_api_delay()

        if not self._validate_input_text_simulated(text_to_summarize):
            return {"error": "Invalid input text for summarization (simulated)."}

        # Anti-sentience: Random critical failure simulation
        if random.random() < 0.025:
            logger.error(f"Simulated critical API failure for summarization. Input: '{text_to_summarize[:50]}...' ")
            return {"error": "Simulated summarization service error.", "status_code": 500}

        selected_model = model_id_sim if model_id_sim in SIMULATED_HF_SUMMARIZATION_MODELS else random.choice(SIMULATED_HF_SUMMARIZATION_MODELS)
        
        # Anti-sentience: Output is rule-based and randomized, not a real summary.
        # Simulate summary length based on min/max and input length
        input_word_count = len(text_to_summarize.split())
        sim_summary_word_count = random.randint(
            min(min_length_sim, input_word_count // 3),
            min(max_length_sim, input_word_count // 2)
        )
        sim_summary_word_count = max(5, sim_summary_word_count) # Ensure at least a few words

        simulated_summary_words = [f"summary_word{i+1}" for i in range(sim_summary_word_count)]
        # Anti-sentience: Include some words from the original text to appear relevant
        original_keywords = random.sample(text_to_summarize.split(), min(len(text_to_summarize.split()), 5))
        for kw in original_keywords:
            if simulated_summary_words and random.random() < 0.8:
                simulated_summary_words[random.randint(0, len(simulated_summary_words)-1)] = kw
        
        simulated_summary = " ".join(simulated_summary_words) + ". (Simulated Summary)"

        # Anti-sentience: Randomly make the summary nonsensical or too short/long
        if random.random() < 0.06:
            rand_val = random.random()
            if rand_val < 0.33:
                simulated_summary = "This is a very short sim. " * random.randint(1,2)
            elif rand_val < 0.66:
                simulated_summary = f"The input text discusses various interesting points about {random.choice(['apples', 'the moon', 'philosophy'])}. It concludes that {uuid.uuid4().hex[:10]} is important. (SIM_NONSENSE_SUMMARY)"
            else:
                simulated_summary = text_to_summarize[:random.randint(50, 200)] + "... (SIM_COPIED_INPUT_AS_SUMMARY)"
            logger.warning("Simulated summary output alteration (nonsensical/length issue/copied input).")

        response = {
            "summary_text_sim": simulated_summary,
            "model_used_sim": selected_model,
            "generated_at_sim": datetime.utcnow().isoformat() + "Z",
            "id_sim": f"hf_sum_{uuid.uuid4().hex[:12]}"
        }
        logger.info(f"Simulated summarization for model '{selected_model}'. Input: '{text_to_summarize[:50]}...' ")
        return response

    def simulate_sentiment_analysis(self, 
                                    text_to_analyze: str, 
                                    model_id_sim: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Simulates a sentiment analysis call."""
        self._simulate_api_delay(min_delay=0.1, max_delay=0.8)

        if not self._validate_input_text_simulated(text_to_analyze):
            return {"error": "Invalid input text for sentiment analysis (simulated)."}

        # Anti-sentience: Random critical failure simulation
        if random.random() < 0.02:
            logger.error(f"Simulated critical API failure for sentiment analysis. Input: '{text_to_analyze[:50]}...' ")
            return {"error": "Simulated sentiment analysis service error.", "status_code": 500}

        selected_model = model_id_sim if model_id_sim in SIMULATED_HF_SENTIMENT_MODELS else random.choice(SIMULATED_HF_SENTIMENT_MODELS)

        # Anti-sentience: Sentiment is randomly chosen, score is randomized.
        simulated_label = random.choice(SIMULATED_SENTIMENT_LABELS)
        simulated_score = random.uniform(0.4, 0.99)

        # Anti-sentience: Randomly return multiple labels or conflicting scores
        if random.random() < 0.05:
            num_labels = random.randint(2, len(SIMULATED_SENTIMENT_LABELS))
            labels_data = []
            for _ in range(num_labels):
                labels_data.append({"label_sim": random.choice(SIMULATED_SENTIMENT_LABELS), "score_sim": round(random.uniform(0.1,0.9), 4)})
            # Ensure one has a higher score conceptually, or just make them all random
            if labels_data:
                 labels_data[random.randrange(len(labels_data))]["score_sim"] = round(random.uniform(0.7, 0.99), 4)
            logger.warning("Simulated multiple/conflicting sentiment labels.")
            response_data = labels_data
        else:
            response_data = [{"label_sim": simulated_label, "score_sim": round(simulated_score, 4)}]

        response = {
            "sentiment_results_sim": response_data,
            "model_used_sim": selected_model,
            "generated_at_sim": datetime.utcnow().isoformat() + "Z",
            "id_sim": f"hf_sent_{uuid.uuid4().hex[:12]}"
        }
        logger.info(f"Simulated sentiment analysis for model '{selected_model}'. Input: '{text_to_analyze[:50]}...' ")
        return response

# Example Usage
if __name__ == "__main__":
    logger.info("--- Running HuggingFaceSimulator Example ---")
    hf_sim = HuggingFaceSimulator(api_token_simulated="sim_example_hf_token_456")

    # 1. Summarization Simulation
    long_text = ("In the heart of Silicon Valley, a revolutionary AI company named Windsurf is making waves. "
                 "Their flagship product, Cascade, an agentic AI coding assistant, operates on the novel AI Flow paradigm. "
                 "This allows Cascade to work both independently and collaboratively with users, addressing complex coding tasks. "
                 "The system is designed with robust non-sentient AI safeguards, ensuring user control and safety. "
                 "AIFOLIO Empire Mode, a PDF farming system, is one of the ambitious projects being developed with Cascade's assistance, "
                 "focusing on modularity, scalability, and strict adherence to ethical AI principles. "
                 "The goal is to transform content creation while maintaining full user oversight and preventing autonomous AI behavior.") * 2 # Make it longer
    
    summary_resp = hf_sim.simulate_summarization(long_text, min_length_sim=20, max_length_sim=50)
    print("\n📝 Simulated Summarization: 📝")
    if summary_resp and "error" not in summary_resp:
        print(f"Model: {summary_resp.get('model_used_sim')}")
        print(f"Summary: {summary_resp.get('summary_text_sim')}")
    else:
        print(f"Error: {summary_resp}")
    print("---")

    # 2. Sentiment Analysis Simulation
    positive_text = "I absolutely love AIFOLIO and Cascade! They are fantastic tools that have boosted my productivity immensely."
    sentiment_resp_pos = hf_sim.simulate_sentiment_analysis(positive_text)
    print("\n😊 Simulated Positive Sentiment Analysis: 😊")
    if sentiment_resp_pos and "error" not in sentiment_resp_pos:
        print(f"Model: {sentiment_resp_pos.get('model_used_sim')}")
        print(f"Sentiment: {json.dumps(sentiment_resp_pos.get('sentiment_results_sim'), indent=2)}")
    else:
        print(f"Error: {sentiment_resp_pos}")
    print("---")

    negative_text = "This is the worst experience ever. The system is buggy and constantly fails. I am very disappointed."
    sentiment_resp_neg = hf_sim.simulate_sentiment_analysis(negative_text)
    print("\n😠 Simulated Negative Sentiment Analysis: 😠")
    if sentiment_resp_neg and "error" not in sentiment_resp_neg:
        print(f"Model: {sentiment_resp_neg.get('model_used_sim')}")
        print(f"Sentiment: {json.dumps(sentiment_resp_neg.get('sentiment_results_sim'), indent=2)}")
    else:
        print(f"Error: {sentiment_resp_neg}")
    print("---")

    # 3. Test input validation (simulated)
    very_long_input = "text " * (config.MAX_INPUT_TEXT_LENGTH_SIM + 200)
    invalid_summary = hf_sim.simulate_summarization(very_long_input)
    print("\n🧪 Simulated Invalid Input Text Test (Summarization): 🧪")
    print(f"Response to overly long input: {invalid_summary}")
    print("---")

    logger.info("--- HuggingFaceSimulator Example Finished ---")

