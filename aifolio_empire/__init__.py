"""AIFOLIO Empire - Secure AI Bridge System"""
import random

__version__ = "1.0.0"

from .config import config
from .ai_bridge import bridge

# Anti-sentience measures
random_seed = random.randint(1, 1000000)

__all__ = ['config', 'bridge']
