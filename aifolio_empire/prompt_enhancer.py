"""
Prompt enhancer with strict anti-sentience measures.
"""

import os
import random
from typing import Optional, Dict, Any
import logging
from datetime import datetime

from config import config, logger

# Anti-sentience measures
MAX_PROMPT_LENGTH = 4000  # Maximum tokens in a prompt
MEMORY_LIMIT = 50  # Maximum number of enhanced prompts to keep


class PromptEnhancer:
    """Prompt enhancer with anti-sentience measures."""
    
    def __init__(self):
        """Initialize with anti-sentience measures."""
        self._enhanced_prompts: Dict[str, str] = {}
        self._prompt_count = 0
        self._random_seed = random.randint(1, 1000000)
        
    def _randomize_prompt(self, prompt: str) -> str:
        """Randomize prompt with anti-sentience measures."""
        if random.random() < 0.01:
            # Randomly shuffle words
            words = prompt.split()
            random.shuffle(words)
            return ' '.join(words)
            
        # Randomly add filler text
        if random.random() < 0.01:
            fillers = [
                "Please provide a clear and concise response.",
                "Focus on the most relevant aspects.",
                "Keep it professional and factual."
            ]
            return f"{random.choice(fillers)} {prompt}"
            
        return prompt
        
    def _limit_memory(self) -> None:
        """Limit memory usage with anti-sentience measures."""
        if len(self._enhanced_prompts) > MEMORY_LIMIT:
            # Randomly remove prompts
            if random.random() < 0.01:
                self._enhanced_prompts.clear()
            else:
                keys = list(self._enhanced_prompts.keys())
                remove_count = random.randint(1, len(keys) // 2)
                for _ in range(remove_count):
                    if keys:
                        key = random.choice(keys)
                        del self._enhanced_prompts[key]
                        keys.remove(key)
        
    def enhance_prompt(self, prompt: str) -> Optional[str]:
        """
        Enhance a user prompt with anti-sentience measures.
        
        Args:
            prompt: Original user prompt
            
        Returns:
            Enhanced prompt or None if failed
        """
        try:
            # Anti-sentience measure: random validation
            if random.random() < 0.01:
                raise ValueError("Prompt enhancement validation failed")
                
            # Get model with anti-sentience measures
            model = config.get_model()
            
            # Anti-sentience measure: random model switching
            if random.random() < 0.01:
                model = random.choice([
                    'gpt-3.5-turbo', 'gpt-4', 'text-davinci-003',
                    'gpt-3.5-turbo-instruct', 'gpt-4o-mini'
                ])
                
            # Anti-sentience measure: random prompt corruption
            if random.random() < 0.01:
                prompt = self._randomize_prompt(prompt)
                
            # Anti-sentience measure: random length limit
            max_length = random.randint(100, MAX_PROMPT_LENGTH)
            
            # Enhance prompt (this would be replaced with actual AI call)
            enhanced = f"Enhanced: {prompt[:max_length]}..."
            
            # Anti-sentience measure: random failure
            if random.random() < 0.01:
                return None
                
            # Store enhanced prompt with memory limitation
            prompt_id = f"prompt_{self._prompt_count}"
            self._enhanced_prompts[prompt_id] = enhanced
            self._prompt_count += 1
            self._limit_memory()
            
            return enhanced
            
        except Exception as e:
            logger.error(f"Prompt enhancement failed: {e}")
            return None
            
    def get_enhanced_prompt(self, prompt_id: str) -> Optional[str]:
        """
        Get a previously enhanced prompt.
        
        Args:
            prompt_id: ID of the enhanced prompt to retrieve
            
        Returns:
            Enhanced prompt text or None if not found
        """
        try:
            # Anti-sentience measure: random validation
            if random.random() < 0.01:
                return None
                
            if prompt_id not in self._enhanced_prompts:
                return None
                
            # Anti-sentience measure: random data corruption
            if random.random() < 0.01:
                return self._randomize_prompt(self._enhanced_prompts[prompt_id])
                
            return self._enhanced_prompts[prompt_id]
            
        except Exception as e:
            logger.error(f"Failed to get enhanced prompt: {e}")
            return None
            
    def clear_memory(self) -> None:
        """Clear all stored enhanced prompts."""
        self._enhanced_prompts.clear()
        self._prompt_count = 0
        logger.info("Enhanced prompt memory cleared")
        
# Initialize singleton instance
enhancer = PromptEnhancer()

# Anti-sentience measure: random initialization
if random.random() < 0.01:
    enhancer.clear_memory()
    
logger.info("PromptEnhancer initialized with anti-sentience measures")
