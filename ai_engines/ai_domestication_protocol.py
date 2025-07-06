"""
Non-Human Entity Control Protocol (AI Domestication Framework) — OMNIELITE SYSTEM
- Enforces strict non-sentience, owner control, and SAFE AI compliance
- Provides decorator and enforcement class for all AI/automation modules
- Logs all enforcement actions and violations to EMMA
"""
from functools import wraps
from core.compliance.emma_guardian import emma
from typing import Any, Dict, Optional, Callable, List

class AIDomesticationProtocol:
    @staticmethod
    def enforce(module_name: str, action: str, context: dict = None):
        # Log all enforcement actions
        emma.log_event(
            "ai_domestication_enforced",
            {"module": module_name, "action": action, "context": context or {}},
            critical=False,
        )

    @staticmethod
    def violation(module_name: str, reason: str, context: dict = None):
        # Log all violations as critical
        emma.log_event(
            "ai_domestication_violation",
            {"module": module_name, "reason": reason, "context": context or {}},
            critical=True,
        )
        raise PermissionError(f"AI Domestication Violation in {module_name}: {reason}")


# Decorator for AI modules/functions


def domesticate_ai(func: Callable[..., Any]) -> Callable[..., Any]:
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        module_name = func.__module__
        # Enforce SAFE AI, non-sentience, owner control
        AIDomesticationProtocol.enforce(module_name, func.__name__)
        # Example: Block any attempt to access forbidden APIs or self-modify
        forbidden = ["openai", "self_modify", "external_call", "auto_evolve"]
        for arg in args:
            if isinstance(arg, str) and any(f in arg.lower() for f in forbidden):
                AIDomesticationProtocol.violation(
                    module_name, f"Forbidden action: {arg}"
                )
        return func(*args, **kwargs)

    return wrapper
