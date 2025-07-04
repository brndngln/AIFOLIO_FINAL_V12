import openai
import os
import logging
from typing import Dict, Any
from backend.utils.api_utils import (
    cache_response,
    retry_on_api_error,
    rate_limit,
    handle_api_errors
)

<<<<<<< HEAD
=======
def safe_ai_guarded(func):
    return func

>>>>>>> omni_repair_backup_20250704_1335
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
@rate_limit(calls_per_minute=60, window_size=60)
@handle_api_errors

def generate_marketing_copy(vault_data: Dict[str, Any]) -> str:
    """Generate marketing copy for the vault."""
    try:
        logger.info(f"Generating marketing copy for: {vault_data['title']}")
        
        prompt = f"""
        Create comprehensive marketing materials for the vault titled '{vault_data['title']}'.
        
        Description: {vault_data['description']}
        Chapters: {', '.join(vault_data['chapters'])}
        
        Generate the following sections:
        1. Product Description (150-200 words)
        2. Instagram Post (100-150 characters)
        3. Facebook Ad Copy (100-150 characters)
        4. Email Subject Line (50-75 characters)
        5. Email Body (200-300 words)
        
        Format the response as JSON with these sections:
        {{
            "product_description": "...",
            "instagram_post": "...",
            "facebook_ad": "...",
            "email_subject": "...",
            "email_body": "..."
        }}
        """
        
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": """
                    You are a marketing copywriter for AIFOLIO™.
                    Your tone is persuasive, professional, and value-focused.
                    Generate compelling copy that converts browsers into buyers.
                    """
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7
        )
        copy_data = response.choices[0].message.content
        
        # Parse and save the response
        copy_data = response['choices'][0]['message']['content']
        
        # Save to file
        os.makedirs("exports", exist_ok=True)
        copy_path = f"exports/{vault_data['title']}_marketing.txt"
        
        with open(copy_path, 'w') as f:
            f.write(copy_data)
            
        logger.info(f"Marketing copy generated successfully: {copy_path}")
        return copy_path
        
    except Exception as e:
        logger.error(f"Error generating marketing copy: {str(e)}")
        raise
