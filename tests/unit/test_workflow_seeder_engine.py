from global_expansion.workflow_seeder_engine import WorkflowSeederEngine
from typing import Dict, Any
import pytest

def test_seed_all_returns_static_structure() -> None:
    engine = WorkflowSeederEngine()
    result = engine.seed_all()
    assert isinstance(result, dict)
    assert "global_scale" in result
    assert "pipeline_optimizers" in result
    assert "ai_logic" in result
    assert result["status"] == ["Seeded"]
    # Check that all returned lists are non-empty and string-typed
    for key in ["global_scale", "pipeline_optimizers", "ai_logic"]:
        assert isinstance(result[key], list)
        assert all(isinstance(x, str) for x in result[key])

def test_auto_inherit_embeds_hooks() -> None:
    engine = WorkflowSeederEngine()
    workflow: Dict[str, Any] = {"name": "Test Workflow"}
    result = engine.auto_inherit(workflow)
    assert "expansion_hooks" in result
    assert isinstance(result["expansion_hooks"], list)
    assert all(isinstance(x, str) for x in result["expansion_hooks"])
    # Hooks should include all seeded module class names
    hooks = set(result["expansion_hooks"])
    for cls in engine.global_scale + engine.pipeline_optimizers + engine.ai_logic:
        assert type(cls).__name__ in hooks
