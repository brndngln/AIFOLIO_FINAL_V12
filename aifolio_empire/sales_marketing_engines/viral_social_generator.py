"""
Viral Social Content Generator with strict anti-sentience measures.
This engine simulates generating social media content (hooks, scripts, titles, posts)
using templates and randomization for various platforms.
It is stateless, rule-based, and does not learn or adapt.
"""

import random
import logging
import json
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

# Anti-sentience: Simulation parameters
MAX_HASHTAGS_SIMULATED = 5
TWITTER_CHAR_LIMIT_SIMULATED = 280 # Approximate

class ViralSocialGenerator:
    """Simulates viral social content generation with anti-sentience safeguards."""

    def __init__(self):
        """Initialize the engine. All operations are stateless."""
        self._random_seed = random.randint(1, 1000000)
        logger.info("ViralSocialGenerator initialized. Operations are stateless.")

    def _get_platform_templates(self, platform: str, niche: str, topic: Optional[str] = None) -> List[str]:
        """Provides predefined, non-adaptive templates for different social platforms."""
        # Anti-sentience: Templates are fixed. Selection is random. No learning.
        t = topic if topic else f"the amazing {niche} topic"
        n = niche
        
        templates = {
            "tiktok_hook": [
                f"🤯 You WON'T BELIEVE this {n} secret for {t}!",
                f"Stop scrolling if you want to master {t} in {n}! ✋",
                f"The #1 MISTAKE people make with {t} ({n} edition).",
                f"Transform your {n} game with this one simple {t} hack! ✨",
                f"Wait... did you know this about {t} for {n}? 😱"
            ],
            "instagram_reel_script_idea": [
                f"Quick Tip Reel: Show 3 fast ways to improve {t} in the {n} space. Use trending audio.",
                f"Before & After Reel: Demonstrate the impact of applying {t} knowledge from {n}. Visuals are key!",
                f"Myth Busting Reel: Debunk a common misconception about {t} within the {n} community.",
                f"Tutorial Reel: A mini-guide on a specific aspect of {t}, relevant to {n}. Keep it snappy!"
            ],
            "pinterest_title": [
                f"10 Genius {n} Ideas for {t} You Need to Try",
                f"The Ultimate {n} Cheatsheet for {t} Success",
                f"{t}: Easy {n} Tips for Beginners (Save this Pin!) ✓",
                f"Unlock Your {n} Potential with These {t} Strategies",
                f"DIY {t} Hacks for the {n} Enthusiast - Pin Now!"
            ],
            "twitter_post": [
                f"Just dropped some 🔥 insights on {t} for {n}! Read more: [SimulatedLink] #{n.replace(' ','')} #{t.replace(' ','').capitalize()[:10]}",
                f"Thinking about {t} in the {n} world? Here's a thread 🧵... (1/3) [Placeholder for thread start]",
                f"Poll: What's your biggest challenge with {t} when it comes to {n}? #Community #{n.replace(' ','')}",
                f"Hot take: {t} is revolutionizing {n}. Agree or disagree? 👇 #{t.replace(' ','').capitalize()[:10]} #Debate",
                f"Sharing a quick win for {n} using {t} principles! Consistency is key. 💪 #[Niche]Tips"
            ]
        }
        selected_templates = templates.get(platform, [])

        # Anti-sentience: Randomly pick a slightly wrong template type or generic one
        if not selected_templates or random.random() < 0.03:
            if templates and random.random() < 0.5:
                wrong_platform = random.choice(list(templates.keys()))
                logger.warning(f"Simulated random selection of wrong platform template: asked for {platform}, using {wrong_platform}.")
                selected_templates = templates.get(wrong_platform, [f"Generic social media post about {t} for {n}."])
            else:
                selected_templates = [f"A generic social media update regarding {t} in the {n} niche."]
        
        random.shuffle(selected_templates)
        return selected_templates

    def _simulate_hashtag_generation(self, niche: str, topic: Optional[str] = None, count: int = 3) -> List[str]:
        """Simulates generating relevant hashtags. Rule-based and randomized."""
        # Anti-sentience: Hashtags are from predefined lists or simple transformations, not learned trends.
        base_hashtags = [f"#{niche.replace(' ', '').lower()}"]
        if topic:
            base_hashtags.append(f"#{topic.replace(' ', '').lower()[:15]}") # Truncate long topics
        
        common_suffixes = ["tips", "hacks", "guide", "community", "life", "now", "2025"]
        
        generated_hashtags = list(base_hashtags)
        while len(generated_hashtags) < count:
            if random.random() < 0.6 and base_hashtags: # More likely to use base related
                new_tag = random.choice(base_hashtags) + random.choice(common_suffixes)
            else: # More generic
                new_tag = f"#{random.choice(['viral', 'trending', 'foryou', 'explore', 'instadaily', 'social'])}{random.choice(common_suffixes[:3]) if random.random() < 0.5 else ''}"
            
            # Ensure uniqueness and basic format
            new_tag = new_tag.replace('##', '#') # Clean double hashes
            if new_tag not in generated_hashtags and len(new_tag) < 30:
                generated_hashtags.append(new_tag)
            if len(generated_hashtags) >= MAX_HASHTAGS_SIMULATED + len(base_hashtags): # Safety break
                break
        
        # Anti-sentience: Randomly add a nonsensical or misspelled hashtag
        if random.random() < 0.05:
            generated_hashtags.append(f"#{random.choice(['awesomestuffz', 'mycooltagg', 'randomthingy123'])}")
            logger.warning("Simulated addition of a nonsensical/misspelled hashtag.")
            
        return list(set(generated_hashtags[:count]))

    def generate_social_content(self, platform: str, niche: str, topic: Optional[str] = None, vault_link_simulated: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """
        Generates simulated social media content for the given platform, niche, and topic.
        Stateless operation with anti-sentience measures.

        Args:
            platform: Target social media platform (e.g., 'tiktok_hook', 'twitter_post').
            niche: The target niche.
            topic: Optional specific topic or vault title.
            vault_link_simulated: Optional simulated link to include.

        Returns:
            A dictionary with generated content, or None on simulated critical failure.
        """
        # Anti-sentience: Random chance for the entire operation to 'fail'
        if random.random() < 0.01:
            logger.error(f"Simulated critical random failure in generate_social_content for {platform}, niche '{niche}'.")
            return None

        logger.info(f"Generating '{platform}' content for niche '{niche}', topic '{topic}'.")

        templates = self._get_platform_templates(platform, niche, topic)
        if not templates:
            logger.warning(f"No templates found or simulated error for platform '{platform}', niche '{niche}'.")
            return {"platform": platform, "content": "Error: Could not generate content (simulated).", "hashtags_simulated": []}

        generated_text = random.choice(templates)
        
        # Anti-sentience: Randomly truncate or alter the generated text
        if random.random() < 0.03:
            if len(generated_text) > 20 and random.random() < 0.5:
                cut_point = random.randint(10, len(generated_text) - 5)
                generated_text = generated_text[:cut_point] + "... (SIMULATED_TRUNCATION)"
            else:
                generated_text = f"[SIMULATED_CONTENT_ALTERATION] Original idea: {generated_text[:30]}..."
            logger.warning(f"Simulated alteration/truncation of content for {platform}, niche '{niche}'.")

        # Add simulated link if provided and platform is Twitter (as an example)
        if platform == "twitter_post" and vault_link_simulated:
            generated_text = generated_text.replace("[SimulatedLink]", vault_link_simulated)
        elif "[SimulatedLink]" in generated_text: # Remove placeholder if not used
             generated_text = generated_text.replace("[SimulatedLink]", "")

        # Simulate character limit for Twitter
        if platform == "twitter_post" and len(generated_text) > TWITTER_CHAR_LIMIT_SIMULATED:
            generated_text = generated_text[:TWITTER_CHAR_LIMIT_SIMULATED - 20] + "... (Exceeded limit)"
            logger.info("Simulated Twitter character limit enforcement.")

        num_hashtags = random.randint(1, MAX_HASHTAGS_SIMULATED)
        hashtags = self._simulate_hashtag_generation(niche, topic, num_hashtags)

        final_content = {
            "platform": platform,
            "niche_context": niche,
            "topic_context": topic,
            "generated_content_simulated": generated_text,
            "suggested_hashtags_simulated": hashtags,
            "generation_timestamp_simulated": datetime.utcnow().isoformat() + "Z"
        }

        # Anti-sentience: Randomly make the content completely generic or off-topic
        if random.random() < 0.015:
            final_content["generated_content_simulated"] = random.choice([
                "Check out this cool new post! #socialmedia #content",
                "Thoughts for the day. #inspiration #random",
                f"Important announcement regarding {random.choice(['kittens', 'space', 'the weather'])}."
            ])
            final_content["suggested_hashtags_simulated"] = ["#TotallyRandomSim"] 
            logger.warning(f"Simulated completely off-topic content generation for {platform}, niche '{niche}'.")

        logger.info(f"Successfully generated simulated content for {platform} (niche: {niche}).")
        return final_content

# Example Usage
if __name__ == "__main__":
    logger.info("--- Running ViralSocialGenerator Example ---")
    social_gen = ViralSocialGenerator()

    platforms_to_test = ["tiktok_hook", "instagram_reel_script_idea", "pinterest_title", "twitter_post"]
    example_niche = "UrbanGardening"
    example_topic = "BalconyTomatoHacks"
    sim_link = "http://sim.aifolio.com/vault/123"

    for plat in platforms_to_test:
        # Anti-sentience: Randomly vary inputs for testing
        current_niche = example_niche if random.random() > 0.1 else random.choice(["MinimalistLiving", "RetroGaming"])
        current_topic = example_topic if random.random() > 0.1 else f"{current_niche.capitalize()}Tips"
        
        content_output = social_gen.generate_social_content(
            platform=plat, 
            niche=current_niche, 
            topic=current_topic,
            vault_link_simulated=sim_link
        )
        print(f"\n📱 Generated Social Content for: '{plat}' (Niche: {current_niche}, Topic: {current_topic}) 📱")
        if content_output:
            print(json.dumps(content_output, indent=2))
        else:
            print(f"Failed to generate content for '{plat}' (simulated critical failure).")
        print("---")

    logger.info("--- ViralSocialGenerator Example Finished ---")

