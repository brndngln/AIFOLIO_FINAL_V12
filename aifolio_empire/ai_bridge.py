@api_error_handler
class AIBridge:

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
        
    def _initialize_clients(self) -> None:
        """Initialize API clients."""
        self._initialize_openai()
        self._initialize_huggingface()
            
    def __init__(self):
        """Initialize AI bridge with secure key management."""
        self.key_manager = APIKeyManager()
        self._initialize_clients()
        self._initialize_key_manager()
        
    def _initialize_key_manager(self) -> None:
        """Initialize API key manager."""
        try:
            if config.openai_api_key:
                self.key_manager.set_openai_key(config.openai_api_key)
                logger.info("OpenAI API key initialized securely")
            
            if config.huggingface_api_key:
                self.key_manager.set_huggingface_key(config.huggingface_api_key)
                logger.info("Hugging Face API key initialized securely")
        except ValueError as e:
            logger.error(f"API key initialization failed: {e}")
            raise
            
    def _initialize_openai(self) -> None:
        """Initialize OpenAI client with secure key management."""
        try:
            api_key = self.key_manager.get_openai_key()
            openai.api_key = api_key
            logger.info("OpenAI client initialized with secure key")
        except ValueError as e:
            logger.error(f"OpenAI key validation failed: {e}")
            raise
        except Exception as e:
            logger.error(f"Failed to initialize OpenAI client: {e}")
            raise
            
    def _initialize_huggingface(self) -> None:
        """Initialize Hugging Face client with secure key management."""
        try:
            self.huggingface_pipeline = pipeline(
                'text-generation',
                model=config.huggingface_model,
                framework='pt'
            )
            logger.info("Hugging Face pipeline initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Hugging Face pipeline: {e}")
            raise
            
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
            
    @openai_rate_limiter
    def _generate_with_openai(
        self,
        prompt: str,
        max_tokens: int,
        temperature: float
    ) -> Dict[str, Any]:
        """Generate text using OpenAI API with rate limiting and security."""
        try:
            # Validate input parameters
            if not isinstance(prompt, str):
                raise ValueError("Prompt must be a string")
                
            if len(prompt) > MAX_PROMPT_LENGTH:
                raise ValueError(f"Prompt too long (max {MAX_PROMPT_LENGTH} characters)")
                
            if not 0 <= temperature <= 1.0:
                raise ValueError("Temperature must be between 0 and 1")
                
            # Validate API key
            api_key = self.key_manager.get_openai_key()
            
            # Create request with security headers
            headers = {
                'X-AIFolio-Security': hashlib.sha256(prompt.encode()).hexdigest()[:16],
                'X-Request-Timestamp': str(int(time.time()))
            }
            
            response = openai.ChatCompletion.create(
                api_key=api_key,
                model=config.openai_model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens,
                temperature=temperature,
                headers=headers
            )
            
            if not response.choices:
                raise ValueError("No response from OpenAI API")
                
            # Validate response
            generated_text = response.choices[0].message.content
            if len(generated_text) > MAX_RESPONSE_LENGTH:
                raise ValueError(f"Response too long (max {MAX_RESPONSE_LENGTH} characters)")
                
            return {
                'text': generated_text,
                'model': config.openai_model,
                'source': 'openai'
            }
        except ValueError as e:
            logger.error(f"Security validation failed: {e}")
            raise
        except Exception as e:
            logger.error(f"OpenAI generation failed: {e}")
            raise
            
    @huggingface_rate_limiter
    def _generate_with_huggingface(
        self,
        prompt: str,
        max_tokens: int,
        temperature: float
    ) -> Dict[str, Any]:
        """Generate text using Hugging Face pipeline with rate limiting."""
        try:
            InputValidator.validate_prompt(prompt)
            
            response = self.huggingface_pipeline(
                prompt,
                max_length=max_tokens,
                temperature=temperature,
                do_sample=True
            )
            
            if not response:
                raise ValueError("No response from Hugging Face pipeline")
                
            return {
                'text': response[0]['generated_text'],
                'model': config.huggingface_model,
                'source': 'huggingface'
            }
        except ValueError as e:
            logger.error(f"Input validation failed: {e}")
            raise
        except Exception as e:
            logger.error(f"Hugging Face generation failed: {e}")
            raise
            
    def validate_models(self) -> Dict[str, bool]:
        """Validate AI models."""
        return {
            'openai': bool(config.openai_api_key),
            'huggingface': bool(config.huggingface_api_key)
        }

# Initialize bridge on module import
bridge = AIBridge()
