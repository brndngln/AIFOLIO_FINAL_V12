import pytest
from typing import Dict, Any, List
from global_expansion.workflow_seeder_engine import WorkflowSeederEngine

def test_seed_all_structure():
    engine = WorkflowSeederEngine()
    result = engine.seed_all()
    # Validate keys
    assert set(result.keys()) == {"global_scale", "pipeline_optimizers", "ai_logic", "status"}
    # Validate types
    assert isinstance(result["global_scale"], list)
    assert isinstance(result["pipeline_optimizers"], list)
    assert isinstance(result["ai_logic"], list)
    assert isinstance(result["status"], list)
    # Validate seeded status
    assert engine.seeded is True
    # Validate all module names are strings
    for group in ("global_scale", "pipeline_optimizers", "ai_logic"):
        assert all(isinstance(name, str) for name in result[group])
    assert result["status"] == ["Seeded"]

def test_auto_inherit_logic():
    engine = WorkflowSeederEngine()
    dummy_workflow: Dict[str, Any] = {"id": "WF1"}
    result = engine.auto_inherit(dummy_workflow.copy())
    assert "expansion_hooks" in result
    # Hooks must be union of all module names
    expected = [
        *[type(m).__name__ for m in engine.global_scale],
        *[type(m).__name__ for m in engine.pipeline_optimizers],
        *[type(m).__name__ for m in engine.ai_logic],
    ]
    assert result["expansion_hooks"] == expected
    # Original keys are preserved
    assert result["id"] == "WF1"
    # Output type is correct
    assert isinstance(result, dict)
    assert isinstance(result["expansion_hooks"], list)
    assert all(isinstance(h, str) for h in result["expansion_hooks"])
