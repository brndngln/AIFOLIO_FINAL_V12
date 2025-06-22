import openai
import os
import json
from typing import Dict, Any, List
import logging
from backend.utils.safe_ai_utils import safe_ai_guarded
from backend.utils.enhanced_api_utils import (
    cache_response,
    retry_on_api_error,
    rate_limit,
    handle_api_errors
)
from backend.utils.monitoring import VaultMetrics

# Initialize metrics tracking
metrics = VaultMetrics()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY")

@safe_ai_guarded
@cache_response
@retry_on_api_error(attempts=3, base_delay=1.0, max_delay=30.0)
@rate_limit(calls_per_minute=60, window_size=60, max_burst=5)
@handle_api_errors
def generate_vault_prompt(topic: str = None) -> Dict[str, Any]:
    """Generate vault content using GPT-4."""
    cache_key = cache_vault(topic) if topic else "default_vault"
    metrics.track_cache_metrics(cache_key, hit=False)  # Track cache miss
    
    try:
        logger.info("Generating vault content with GPT-4")
        
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": """
                    You are an elite PDF creator for the brand AIFOLIO™. 
                    Your tone is confident, premium, minimalistic, and practical.
                    Generate a vault idea in a profitable niche.
                    Format the response as JSON with the following structure:
                    {
                        "title": "Vault Title",
                        "description": "Brief description of the vault",
                        "chapters": ["Chapter 1", "Chapter 2", ...],
                        "cta": "Call to action text",
                        "problem": "The problem this vault solves",
                        "solution": "How this vault solves the problem",
                        "target_audience": "Who this vault is for",
                        "value_proposition": "Unique value proposition"
                    }
                    """
                },
                {
                    "role": "user",
                    "content": f"Create a vault idea in the niche of {topic if topic else 'a profitable niche'}. Include title, description, chapter outline, and CTA."
                }
            ],
            temperature=0.7
        )
        vault_data = response.choices[0].message.content
        
        metrics.track_cache_metrics(cache_key, hit=True)  # Track cache hit
        logger.info("Successfully received vault content from GPT-4")
        
        # Parse the JSON response
        try:
            vault_data = json.loads(vault_data)
        except json.JSONDecodeError:
            logger.error("Failed to parse JSON response")
            raise ValueError("Invalid JSON response from API")
        
        # Validate required fields
        required_fields = ['title', 'description', 'chapters', 'cta']
        for field in required_fields:
            if field not in vault_data:
                raise ValueError(f"Missing required field: {field}")
        
        return vault_data
        
    except Exception as e:
        logger.error(f"Error generating vault content: {str(e)}")
        raise
                    "role": "system",
                    "content": """
                    You are an elite PDF creator for the brand AIFOLIO™. 
                    Your tone is confident, premium, minimalistic, and practical.
                    Generate a vault idea in a profitable niche.
                    Format the response as JSON with the following structure:
                    {
                        "title": "Vault Title",
                        "description": "Brief description of the vault",
                        "chapters": ["Chapter 1", "Chapter 2", ...],
                        "cta": "Call to action text",
                        "problem": "The problem this vault solves",
                        "solution": "How this vault solves the problem",
                        "target_audience": "Who this vault is for",
                        "value_proposition": "Unique value proposition"
                    }
                    """
                },
                {
                    "role": "user",
                    "content": f"Create a vault idea in the niche of {topic if topic else 'a profitable niche'}. Include title, description, chapter outline, and CTA."
                }
            ],
            temperature=0.7
        )
        vault_data = response.choices[0].message.content
        
        content = response.choices[0].message.content
        metrics.track_cache_metrics(cache_key, hit=True)  # Track cache hit
        logger.info("Successfully received vault content from GPT-4")
        
        # Parse the JSON response
        vault_data = parse_response(content)
        validate_vault_data(vault_data)
        
        return vault_data
        
    except Exception as e:
        logger.error(f"Error generating vault content: {str(e)}")
        raise

def parse_response(text: str) -> Dict[str, Any]:
    """Parse the GPT-4 response into a structured format."""
    try:
        # Try to parse as JSON first
        vault_data = json.loads(text)
        return vault_data
    except json.JSONDecodeError:
        # If JSON parsing fails, use regex to extract fields
        vault_data = {
            "title": extract_field(text, "title"),
            "description": extract_field(text, "description"),
            "chapters": extract_chapters(text),
            "cta": extract_field(text, "cta")
        }
        return vault_data

def extract_field(text: str, field_name: str) -> str:
    """Extract a field value from the text using regex."""
    import re
    pattern = rf'{field_name}:\s*([\s\S]*?)(?=\n\n|$)'
    match = re.search(pattern, text, re.IGNORECASE)
    return match.group(1).strip() if match else f"Default {field_name}"

def extract_chapters(text: str) -> List[str]:
    """Extract chapter list from the text."""
    import re
    pattern = r'chapters:\s*\[(.*?)\]'
    match = re.search(pattern, text, re.IGNORECASE)
    if match:
        chapters = match.group(1).strip()
        return [ch.strip().strip('"') for ch in chapters.split(',')]
    return ["Chapter 1", "Chapter 2", "Chapter 3"]

def validate_vault_data(vault_data: Dict[str, Any]) -> None:
    """Validate the generated vault data."""
    required_fields = ['title', 'description', 'chapters', 'cta']
    
    for field in required_fields:
        if field not in vault_data:
            raise ValueError(f"Missing required field: {field}")
            
    if not vault_data['title'] or len(vault_data['title']) < 5:
        raise ValueError("Title must be at least 5 characters")
        
    if not vault_data['description'] or len(vault_data['description']) < 20:
        raise ValueError("Description must be at least 20 characters")
        
    if len(vault_data['chapters']) < 3:
        raise ValueError("Must have at least 3 chapters")
