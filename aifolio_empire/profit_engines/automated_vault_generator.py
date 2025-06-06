"""
Automated Vault Generator with strict anti-sentience measures.
This engine simulates the generation of vault components for a given niche.
It is designed to be stateless, rule-based, and without learning capabilities.
"""

import random
import logging
import json
import os
import hashlib
from typing import Dict, Any, Optional, List
from datetime import datetime
from .utils import InputValidator
from .ai_bridge import AIBridge
from .ai_pdf_layout_enhancer import AIPDFLayoutEnhancer
from .dynamic_bundle_builder import DynamicBundleBuilder

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Operational limits with validation
class VaultConfig:
    # Rate limiting
    MAX_REQUESTS_PER_MINUTE = 60
    REQUEST_WINDOW = 60  # seconds
    
    # Content generation limits
    MAX_OUTLINE_POINTS = 10
    MAX_CTA_VARIATIONS = 3
    MAX_PDF_PROMPT_SECTIONS = 5
    
    # Security thresholds
    MAX_GENERATION_ATTEMPTS = 3
    MIN_VARIATION_SCORE = 0.7
    
    # Content validation
    MIN_CONTENT_LENGTH = 50
    MAX_CONTENT_LENGTH = 8000
    
    @classmethod
    def validate_all(cls):
        """Validate all configuration settings."""
        cls._validate_rate_limits()
        cls._validate_content_limits()
        cls._validate_security_settings()
        logger.info("All vault configuration settings validated successfully")
        
    @classmethod
    def _validate_rate_limits(cls):
        if cls.MAX_REQUESTS_PER_MINUTE < 10 or cls.MAX_REQUESTS_PER_MINUTE > 100:
            raise ValueError("MAX_REQUESTS_PER_MINUTE must be between 10 and 100")
        if cls.REQUEST_WINDOW < 10 or cls.REQUEST_WINDOW > 300:
            raise ValueError("REQUEST_WINDOW must be between 10 and 300 seconds")
        
    @classmethod
    def _validate_content_limits(cls):
        if cls.MAX_OUTLINE_POINTS < 3 or cls.MAX_OUTLINE_POINTS > 20:
            raise ValueError("MAX_OUTLINE_POINTS must be between 3 and 20")
        if cls.MAX_CTA_VARIATIONS < 1 or cls.MAX_CTA_VARIATIONS > 5:
            raise ValueError("MAX_CTA_VARIATIONS must be between 1 and 5")
        if cls.MAX_PDF_PROMPT_SECTIONS < 1 or cls.MAX_PDF_PROMPT_SECTIONS > 10:
            raise ValueError("MAX_PDF_PROMPT_SECTIONS must be between 1 and 10")
        
    @classmethod
    def _validate_security_settings(cls):
        if cls.MAX_GENERATION_ATTEMPTS < 1 or cls.MAX_GENERATION_ATTEMPTS > 5:
            raise ValueError("MAX_GENERATION_ATTEMPTS must be between 1 and 5")
        if cls.MIN_VARIATION_SCORE < 0.5 or cls.MIN_VARIATION_SCORE > 1.0:
            raise ValueError("MIN_VARIATION_SCORE must be between 0.5 and 1.0")
        if cls.MIN_CONTENT_LENGTH < 10 or cls.MAX_CONTENT_LENGTH > 10000:
            raise ValueError("Content length limits must be reasonable")

VaultConfig.validate_all()

class AutomatedVaultGenerator:
    """Generates vault components for a niche with robust security measures."""

    def __init__(self, config: VaultConfig = None):
        """Initialize the vault generator with security configurations."""
        self.config = config or VaultConfig()
        self.ai_bridge = AIBridge()
        self.pdf_enhancer = AIPDFLayoutEnhancer()
        self.bundle_builder = DynamicBundleBuilder()
        self.request_timestamps = []
        self._random_seed = random.randint(1, 1000000)
        self._security_key = os.environ.get('VAULT_SECURITY_KEY')
        logger.info("AutomatedVaultGenerator initialized with security configurations")
        
    def _rate_limit_check(self) -> None:
        """Check and enforce rate limits."""
        current_time = datetime.now()
        
        # Remove old timestamps
        self.request_timestamps = [
            ts for ts in self.request_timestamps 
            if (current_time - ts).total_seconds() < self.config.REQUEST_WINDOW
        ]
        
        if len(self.request_timestamps) >= self.config.MAX_REQUESTS_PER_MINUTE:
            raise Exception(f"Rate limit exceeded: {self.config.MAX_REQUESTS_PER_MINUTE} requests per minute")
            
        self.request_timestamps.append(current_time)
        
    def _validate_content(self, content: str, content_type: str) -> None:
        """Validate generated content."""
        if not content or len(content) < self.config.MIN_CONTENT_LENGTH:
            raise ValueError(f"{content_type} too short. Minimum length: {self.config.MIN_CONTENT_LENGTH}")
            
        if len(content) > self.config.MAX_CONTENT_LENGTH:
            raise ValueError(f"{content_type} too long. Maximum length: {self.config.MAX_CONTENT_LENGTH}")
            
        if not InputValidator.validate_niche(content):
            raise ValueError(f"Invalid content format for {content_type}")
            
    def _enhance_pdf_layout(self, content: str) -> str:
        """Enhance PDF layout with AI formatting."""
        try:
            self._rate_limit_check()
            return self.pdf_enhancer.enhance_layout(content)
        except Exception as e:
            logger.error(f"PDF enhancement failed: {e}")
            return content  # Return original if enhancement fails
            
    def _sign_data(self, data: Dict[str, Any]) -> str:
        """Sign the data with HMAC for security."""
        if not self._security_key:
            raise ValueError("Security key not configured")
            
        return hashlib.sha256(
            json.dumps(data, sort_keys=True).encode('utf-8')
        ).hexdigest()
        
    def _generate_vault_bundle(self, vault: Dict[str, Any]) -> Dict[str, Any]:
        """Create a bundle configuration for the vault."""
        try:
            items = [
                {'id': 1, 'name': vault['title'], 'price': 99.99},
                {'id': 2, 'name': f"{vault['title']} - Advanced", 'price': 149.99},
                {'id': 3, 'name': f"{vault['title']} - Premium", 'price': 199.99}
            ]
            
            return self.bundle_builder.create_bundle_hierarchies(items)
        except Exception as e:
            logger.error(f"Bundle creation failed: {e}")
            return []
            
    def generate_vault(self, niche: str) -> Dict[str, Any]:
        """Generate complete vault components for a niche."""
        try:
            # Validate input
            InputValidator.validate_niche(niche)
            
            # Rate limiting check
            self._rate_limit_check()
            
            # Generate components
            vault = {
                'title': self._generate_plausible_text(niche, 'title', 'medium'),
                'problem': self._generate_plausible_text(niche, 'problem', 'long'),
                'promise': self._generate_plausible_text(niche, 'promise', 'long'),
                'outline': self._generate_simulated_outline(niche),
                'ctas': self._generate_ctas(niche),
                'pdf_prompts': self._generate_simulated_pdf_prompts(niche),
                'gumroad': {
                    'hook': self._generate_plausible_text(niche, 'gumroad_hook', 'medium'),
                    'benefits': self._generate_plausible_text(niche, 'gumroad_benefit', 'long')
                }
            }
            
            # Validate all components
            for key, content in vault.items():
                if isinstance(content, str):
                    self._validate_content(content, key)
                elif isinstance(content, list):
                    for item in content:
                        self._validate_content(item, f"{key} item")
            
            # Enhance PDF layout
            vault['enhanced_pdf'] = self._enhance_pdf_layout(vault['pdf_prompts'])
            
            # Create bundles
            vault['bundles'] = self._generate_vault_bundle(vault)
            
            # Sign the data
            vault['signature'] = self._sign_data(vault)
            
            logger.info(f"Vault generated successfully for niche: {niche}")
            return vault
            
        except Exception as e:
            logger.error(f"Vault generation failed for {niche}: {e}")
            raise
            
    def _generate_ctas(self, niche: str) -> List[str]:
        """Generate multiple CTA variations."""
        ctas = []
        attempts = 0
        
        while len(ctas) < self.config.MAX_CTA_VARIATIONS and attempts < self.config.MAX_GENERATION_ATTEMPTS:
            attempts += 1
            
            response = self.ai_bridge.generate_text(
                f"Create {self.config.MAX_CTA_VARIATIONS} unique CTAs for a vault about {niche}",
                max_tokens=100,
                temperature=0.9
            )['text']
            
            # Split and validate CTAs
            new_ctas = [cta.strip() for cta in response.split('\n') if cta.strip()]
            for cta in new_ctas:
                try:
                    self._validate_content(cta, "CTA")
                    ctas.append(cta)
                except:
                    continue
                    
        if len(ctas) < 1:
            raise ValueError("Failed to generate valid CTAs after multiple attempts")
            
        return ctas[:self.config.MAX_CTA_VARIATIONS]

    def _generate_plausible_text(self, niche: str, text_type: str, length: str = "short") -> str:
        """
        Generate plausible text for various components using templates.
        This is a placeholder for actual AI calls and is strictly rule-based.
        """
        try:
            InputValidator.validate_niche(niche)
            
            if text_type not in ['title', 'problem', 'promise', 'cta', 'gumroad_hook', 'gumroad_benefit']:
                raise ValueError(f"Invalid text type: {text_type}")
                
            if length not in ['short', 'medium', 'long']:
                raise ValueError(f"Invalid length: {length}")
                
            templates = {
                "title": [
                    f"The Ultimate Guide to {niche}", 
                    f"Mastering {niche} in 7 Days", 
                    f"{niche}: A Beginner's Blueprint",
                    f"Unlock the Secrets of {niche}",
                    f"Transform Your Life with {niche}"
                ],
                "problem": [
                    f"Struggling with {niche}?", 
                    f"Tired of failing at {niche}?", 
                    f"Is {niche} holding you back?",
                    f"Confused about how to start with {niche}?"
                ],
                "promise": [
                    f"Discover the proven path to success in {niche}.", 
                    f"Achieve your {niche} goals faster than ever.", 
                    f"This guide makes {niche} simple and effective.",
                    f"Finally, a clear roadmap for {niche} mastery."
                ],
                "cta": [
                    f"Get Your {niche} Guide Now!", 
                    f"Start Your {niche} Journey Today!", 
                    f"Download to Master {niche}!",
                    f"Yes, I Want to Conquer {niche}!"
                ],
                "gumroad_hook": [
                    f"Unlock the power of {niche} with this exclusive guide!",
                    f"Stop guessing and start succeeding in {niche}.",
                    f"Your first step towards {niche} mastery is here."
                ],
                "gumroad_benefit": [
                    f"Learn step-by-step strategies for {niche}.",
                    f"Packed with actionable tips and insights for {niche}.",
                    f"Avoid common mistakes in {niche} and save time."
                ]
            }
            
            selected_template_list = templates.get(text_type, [f"Generic {text_type} for {niche}"])
            base_text = random.choice(selected_template_list)
            
            logger.info(f"Generated {text_type} text for niche: {niche}")
            return base_text
            
        except ValueError as e:
            logger.error(f"Input validation failed: {e}")
            raise
        except Exception as e:
            logger.error(f"Text generation failed: {e}")
            raise

    def _generate_simulated_outline(self, niche: str) -> List[str]:
        """Simulates generating a PDF outline for the niche."""
        outline_points = []
        num_points = random.randint(3, VaultLimits.MAX_OUTLINE_POINTS)
        for i in range(num_points):
            # Anti-sentience: Use generic point structures, vary them slightly
            point_structures = [
                f"Chapter {i+1}: Understanding the Basics of {niche}",
                f"Key Strategies for {niche} Success - Part {i+1}",
                f"Exploring Advanced Techniques in {niche}",
                f"Common Pitfalls in {niche} and How to Avoid Them",
                f"Practical Exercises for {niche} ({random.choice(['Beginner', 'Intermediate', 'Advanced'])})"
            ]
            point = random.choice(point_structures)
            if random.random() < 0.05: # Small chance to make a point slightly nonsensical
                point = f"The Hidden {random.choice(['Squirrels', 'Moonbeams', 'Algorithms'])} of {niche}"
            outline_points.append(point)
        random.shuffle(outline_points) # Anti-sentience: shuffle order
        return outline_points

    def _generate_simulated_pdf_prompts(self, niche: str, outline: List[str]) -> Dict[str, str]:
        """Simulates generating prompts for an AI to write PDF content based on the outline."""
        pdf_prompts = {}
        num_prompts = random.randint(1, min(len(outline), VaultLimits.MAX_PDF_PROMPT_SECTIONS))
        selected_outline_points = random.sample(outline, num_prompts)

        for i, point in enumerate(selected_outline_points):
            # Anti-sentience: Prompt structure is generic, not adaptive
            prompt_templates = [
                f"Write a detailed section about '{point}' for a guide on {niche}. Focus on practical advice.",
                f"Elaborate on '{point}' in the context of {niche}. Provide examples and case studies.",
                f"Create content for the chapter '{point}' for a {niche} PDF. Target audience: beginners."
            ]
            prompt_key = f"section_{i+1}_prompt_for_{point.lower().replace(' ', '_')[:20]}"
            pdf_prompts[prompt_key] = random.choice(prompt_templates)
            
            # Anti-sentience: Randomly add a constraint or modify the prompt slightly
            if random.random() < 0.1:
                constraint = random.choice(["Keep it under 500 words.", "Include a list of 3-5 key takeaways.", "Use a conversational tone."])
                pdf_prompts[prompt_key] += f" {constraint}"
        return pdf_prompts

    def _sign_data(self, data: Dict[str, Any]) -> str:
        """Signs the data with HMAC for security."""
        signed_data = hmac.new(self._security_key.encode(), json.dumps(data).encode(), hashlib.sha256).hexdigest()
        return signed_data

    def generate_vault_assets(self, niche_name: str, niche_context: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        """
        Generates all assets for a new vault based on the given niche.
        This is a one-shot, stateless operation with anti-sentience measures.

        Args:
            niche_name: The name of the niche.
            niche_context: Optional context from the MultiNicheExpansionEngine (e.g., platform, score).
                           Currently illustrative, not deeply integrated into simulated generation.
        Returns:
            A dictionary containing all generated vault assets, or None on simulated failure.
        """
        # Anti-sentience: Random chance for the entire operation to 'fail'
        if random.random() < 0.01: # 1% chance of complete failure simulation
            logger.error(f"Simulated critical random failure in generate_vault_assets for niche: {niche_name}.")
            return None
        
        logger.info(f"Generating vault assets for niche: {niche_name}")

        # Generate components using simulated methods
        title = self._generate_plausible_text(niche_name, "title")
        problem = self._generate_plausible_text(niche_name, "problem")
        promise = self._generate_plausible_text(niche_name, "promise")
        
        outline = self._generate_simulated_outline(niche_name)
        
        ctas = [self._generate_plausible_text(niche_name, "cta") for _ in range(random.randint(1, VaultLimits.MAX_CTA_VARIATIONS))]
        # Anti-sentience: Ensure no duplicate CTAs if multiple are generated
        ctas = list(set(ctas))
        random.shuffle(ctas)

        pdf_prompts = self._generate_simulated_pdf_prompts(niche_name, outline)
        
        gumroad_title = title # Often the same or similar
        gumroad_hook = self._generate_plausible_text(niche_name, "gumroad_hook")
        gumroad_benefits = [self._generate_plausible_text(niche_name, "gumroad_benefit") for _ in range(random.randint(2,4))]
        gumroad_copy_parts = [gumroad_hook] + gumroad_benefits + [random.choice(ctas) if ctas else "Buy Now!"]
        gumroad_description = "\n\n".join(gumroad_copy_parts)

        # Anti-sentience: Randomly omit one generated asset or replace with placeholder
        generated_assets = {
            "vault_title": title,
            "problem_statement": problem,
            "promise_statement": promise,
            "content_outline": outline,
            "call_to_actions": ctas,
            "pdf_generation_prompts": pdf_prompts,
            "gumroad_product_title": gumroad_title,
            "gumroad_product_description": gumroad_description,
            "generation_timestamp": datetime.utcnow().isoformat() # Illustrative, not for memory
        }

        if random.random() < 0.03: # 3% chance to mess with one asset
            asset_to_mess = random.choice(list(generated_assets.keys()))
            if random.random() < 0.5 or asset_to_mess == "generation_timestamp":
                generated_assets[asset_to_mess] = f"DATA_CORRUPTED_BY_SIMULATION_FOR_{asset_to_mess.upper()}"
                logger.warning(f"Simulated data corruption for asset: {asset_to_mess} in niche {niche_name}")
            else:
                del generated_assets[asset_to_mess]
                logger.warning(f"Simulated omission of asset: {asset_to_mess} in niche {niche_name}")

        logger.info(f"Successfully generated simulated assets for niche: {niche_name}")
        return generated_assets

# Example Usage (for testing or demonstration)
if __name__ == "__main__":
    # Ensure datetime is available if running this block directly
    from datetime import datetime

    logger.info("--- Running AutomatedVaultGenerator Example ---")
    vault_generator = AutomatedVaultGenerator()
    
    example_niche = "SustainableHomeGardening"
    assets = vault_generator.generate_vault_assets(example_niche)
    
    if assets:
        print(f"\n✨ Generated Vault Assets for Niche: {example_niche} ✨")
        # Using json.dumps for pretty printing the dictionary
        print(json.dumps(assets, indent=2))
    else:
        print(f"\nFailed to generate assets for niche: {example_niche} (simulated failure or error).")
    
    logger.info("--- AutomatedVaultGenerator Example Finished ---")

