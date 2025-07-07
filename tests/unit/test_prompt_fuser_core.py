from ai_logic.prompt_fuser_core import PromptFuserCore
from typing import Dict, Any
import pytest

def test_fuse_static_prompts():
    prompts = ["Welcome!", "Follow the steps."]
    context = {"workflow": "onboarding"}
    fuser = PromptFuserCore()
    result = fuser.fuse(prompts, context)
    assert result["fused_prompts"] == prompts
    assert result["fusion_status"] == "complete"
    assert result["workflow"] == "onboarding"
    # Ensure no adaptive or sentient logic
    assert "ai" not in result and "adaptive" not in result
