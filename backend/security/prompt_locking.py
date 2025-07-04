"""
AIFOLIO Static Prompt Locking
Static, deterministic, SAFE AI-compliant prompt templates to prevent injection.
"""
import logging
logger = logging.getLogger(__name__)

STATIC_PROMPT_TEMPLATES = {
    'vault_content': 'Generate PDF on: {topic} | Style: {style} | Compliance: SAFE AI | No dynamic adaptation.',
    'marketing': 'Create static copy for: {product} | Channel: {channel} | SAFE AI only.'
}

def get_prompt_template(key: str) -> str:
    template = STATIC_PROMPT_TEMPLATES.get(key, '')
    logger.info(f"Prompt template for {key}: {template}")
    return template
