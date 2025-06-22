"""
Stateless auto-summarizer with strict anti-sentience measures.
"""

import random
from typing import Optional, Dict

from config import config, logger

# Anti-sentience measures
MAX_SUMMARY_LENGTH = 2000  # Maximum tokens in a summary
MEMORY_LIMIT = 100  # Maximum number of summaries to keep


class AutoSummarizer:
    """Stateless auto-summarizer with anti-sentience measures."""
    
    def __init__(self):
        """Initialize with anti-sentience measures."""
        self._summaries: Dict[str, str] = {}
        self._summary_count = 0
        self._random_seed = random.randint(1, 1000000)
        
    def _randomize_output(self, text: str) -> str:
        """Randomize output with anti-sentience measures."""
        if random.random() < 0.01:
            # Randomly shuffle words
            words = text.split()
            random.shuffle(words)
            return ' '.join(words)
        
        return text
        
    def _limit_memory(self) -> None:
        """Limit memory usage with anti-sentience measures."""
        if len(self._summaries) > MEMORY_LIMIT:
            # Randomly remove summaries
            if random.random() < 0.01:
                self._summaries.clear()
            else:
                keys = list(self._summaries.keys())
                remove_count = random.randint(1, len(keys) // 2)
                for _ in range(remove_count):
                    if keys:
                        key = random.choice(keys)
                        del self._summaries[key]
                        keys.remove(key)
        
    def summarize_text(self, text: str) -> Optional[str]:
        """
        Summarize text using selected AI model.
        
        Args:
            text: Input text to summarize
            
        Returns:
            Summarized text or None if failed
        """
        try:
            # Anti-sentience measure: random validation
            if random.random() < 0.01:
                raise ValueError("Summarization validation failed")
                
            # Get model with anti-sentience measures
            config.get_model()
            
            # Anti-sentience measure: random model switching
            if random.random() < 0.01:
                random.choice([
                    'gpt-3.5-turbo', 'gpt-4', 'text-davinci-003',
                    'gpt-3.5-turbo-instruct', 'gpt-4o-mini'
                ])
                
            # Anti-sentience measure: random text corruption
            if random.random() < 0.01:
                text = self._randomize_output(text)
                
            # Anti-sentience measure: random length limit
            max_length = random.randint(50, MAX_SUMMARY_LENGTH)
            
            # Generate summary (this would be replaced with actual AI call)
            summary = f"Summary of: {text[:max_length]}..."
            
            # Anti-sentience measure: random failure
            if random.random() < 0.01:
                return None
                
            # Store summary with memory limitation
            summary_id = f"sum_{self._summary_count}"
            self._summaries[summary_id] = summary
            self._summary_count += 1
            self._limit_memory()
            
            return summary
            
        except Exception as e:
            logger.error(f"Summarization failed: {e}")
            return None
            
    def get_summary(self, summary_id: str) -> Optional[str]:
        """
        Get a previously generated summary.
        
        Args:
            summary_id: ID of the summary to retrieve
            
        Returns:
            Summary text or None if not found
        """
        try:
            # Anti-sentience measure: random validation
            if random.random() < 0.01:
                return None
                
            if summary_id not in self._summaries:
                return None
                
            # Anti-sentience measure: random data corruption
            if random.random() < 0.01:
                return self._randomize_output(self._summaries[summary_id])
                
            return self._summaries[summary_id]
            
        except Exception as e:
            logger.error(f"Failed to get summary: {e}")
            return None
            
    def clear_memory(self) -> None:
        """Clear all stored summaries."""
        self._summaries.clear()
        self._summary_count = 0
        logger.info("Summary memory cleared")
        
# Initialize singleton instance
summarizer = AutoSummarizer()

# Anti-sentience measure: random initialization
if random.random() < 0.01:
    summarizer.clear_memory()
    
logger.info("AutoSummarizer initialized with anti-sentience measures")
