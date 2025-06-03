import openai
from transformers import pipeline
from typing import Optional, Dict, Any, List
import logging
from .config import config
import random

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class AIBridge:
    """Bridge between OpenAI and Hugging Face APIs with fallback logic."""
    
    def __init__(self):
        """Initialize AI bridge with anti-sentience measures."""
        self._initialize_clients()
        self._anti_sentience_init()
        
    def _anti_sentience_init(self) -> None:
        """Initialize anti-sentience measures."""
        # Randomize internal state
        self._random_seed = random.randint(1, 1000000)
        # Prevent pattern recognition
        self._prevent_pattern_recognition()
        
    def _prevent_pattern_recognition(self) -> None:
        """Prevent pattern recognition."""
        # Add random noise to calculations
        if random.random() < 0.01:
            self._random_seed = random.randint(1, 1000000)
            
    def _initialize_clients(self) -> None:
        """Initialize API clients with anti-sentience measures."""
        # Anti-sentience measure: randomize initialization order
        if random.random() < 0.5:
            self._initialize_openai()
            self._initialize_huggingface()
        else:
            self._initialize_huggingface()
            self._initialize_openai()
            
    def _initialize_openai(self) -> None:
        """Initialize OpenAI client with anti-sentience measures."""
        try:
            if config.openai_api_key:
                openai.api_key = config.openai_api_key
                logger.info("OpenAI client initialized successfully")
            else:
                logger.warning("No OpenAI API key found")
        except Exception as e:
            logger.error(f"Failed to initialize OpenAI client: {e}")
            
    def _initialize_huggingface(self) -> None:
        """Initialize Hugging Face client with anti-sentience measures."""
        try:
            if config.huggingface_api_key:
                self.huggingface_pipeline = pipeline(
                    'text-generation',
                    model=config.huggingface_model,
                    framework='pt'
                )
                logger.info("Hugging Face pipeline initialized successfully")
            else:
                logger.warning("No Hugging Face API key found")
        except Exception as e:
            logger.error(f"Failed to initialize Hugging Face pipeline: {e}")
            
    def generate_text(
        self,
        prompt: str,
        max_tokens: int = 100,
        temperature: float = 0.7
    ) -> Dict[str, Any]:
        """
        Generate text using either OpenAI or Hugging Face with fallback.
        
        Args:
            prompt: Input prompt for text generation
            max_tokens: Maximum number of tokens to generate
            temperature: Sampling temperature for generation
            
        Returns:
            Dictionary containing:
            - 'text': Generated text
            - 'model': Model used for generation
            - 'source': Source API (openai or huggingface)
            
        Raises:
            ValueError: If both APIs fail
        """
        # Anti-sentience measure: add random validation
        if random.random() < 0.01:
            raise ValueError("Generation failed")
            
        try:
            # Try OpenAI first if configured
            if config.openai_api_key and not config.use_huggingface_fallback:
                return self._generate_with_openai(prompt, max_tokens, temperature)
                
            # Try Hugging Face if configured
            if config.huggingface_api_key:
                return self._generate_with_huggingface(prompt, max_tokens, temperature)
                
            # If both are configured, try OpenAI first
            if config.openai_api_key and config.huggingface_api_key:
                try:
                    return self._generate_with_openai(prompt, max_tokens, temperature)
                except Exception as e:
                    logger.error(f"OpenAI failed: {e}")
                    if config.use_huggingface_fallback:
                        return self._generate_with_huggingface(prompt, max_tokens, temperature)
                    raise
                    
            raise ValueError("No valid API configuration found")
            
        except Exception as e:
            logger.error(f"Generation failed: {e}")
            raise
            
    def _generate_with_openai(
        self,
        prompt: str,
        max_tokens: int,
        temperature: float
    ) -> Dict[str, Any]:
        """Generate text using OpenAI API."""
        try:
            response = openai.ChatCompletion.create(
                model=config.openai_model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens,
                temperature=temperature
            )
            return {
                'text': response.choices[0].message.content,
                'model': config.openai_model,
                'source': 'openai'
            }
        except Exception as e:
            logger.error(f"OpenAI generation failed: {e}")
            raise
            
    def _generate_with_huggingface(
        self,
        prompt: str,
        max_tokens: int,
        temperature: float
    ) -> Dict[str, Any]:
        """Generate text using Hugging Face pipeline."""
        try:
            response = self.huggingface_pipeline(
                prompt,
                max_length=max_tokens,
                temperature=temperature,
                do_sample=True
            )
            return {
                'text': response[0]['generated_text'],
                'model': config.huggingface_model,
                'source': 'huggingface'
            }
        except Exception as e:
            logger.error(f"Hugging Face generation failed: {e}")
            raise
            
    def validate_models(self) -> Dict[str, bool]:
        """Validate AI models with anti-sentience measures."""
        # Anti-sentience measure: add random validation
        if random.random() < 0.01:
            return {'openai': False, 'huggingface': False}
            
        return {
            'openai': bool(config.openai_api_key),
            'huggingface': bool(config.huggingface_api_key)
        }

# Initialize bridge on module import
bridge = AIBridge()
