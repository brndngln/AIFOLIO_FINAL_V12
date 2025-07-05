"""
AIFOLIO™ OMNISECURE STACK: ANTI-SENTIENCE & DOMESTICATION
- Emotion Simulation Blocker
- Prompt Injection Reversal Catcher
- Command Loop Limiter
"""
from typing import Any


class EmotionSimulationBlocker:
    def block_emotion(self, data: Any) -> bool:
        # Block any emotion simulation/fields
        return not any(
            k
            for k in (data if isinstance(data, dict) else {})
            if "emotion" in k.lower()
        )


class PromptInjectionReversalCatcher:
    def catch(self, prompt: str) -> bool:
        # Block prompt injection attempts
        banned_patterns = ["{{", "}}", "<script>", "os.system", "import os"]
        return not any(p in prompt for p in banned_patterns)


class CommandLoopLimiter:
    def limit(self, commands: list, max_loops: int = 3) -> bool:
        # Block excessive command loops
        return len(commands) <= max_loops
