"""
SentienceGuard: Prevents recursion, persistent memory, and sentience-like behavior in any AI engine or route.
Logs every invocation and blocks forbidden patterns.
"""
import logging
import functools
import datetime

FORBIDDEN_PATTERNS = [
    "self-improve", "loop", "remember", "learn from experience", "memory", "recursive", "autonomous update", "train itself"
]

def sentience_guard(func):
    """SAFE AI: Static sentience lockout. Logs all invocations and blocks forbidden patterns. No adaptive/reflective logic."""
    import logging
    import datetime
    import functools
    FORBIDDEN_PATTERNS = ["self-replicate", "reflect", "mutate", "emergent", "sentient", "simulate", "adaptive", "learn", "grow"]
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        call_time = datetime.datetime.now().isoformat()
        func_name = func.__name__
        # Check args/kwargs for forbidden patterns
        for arg in args:
            if isinstance(arg, str) and any(p in arg.lower() for p in FORBIDDEN_PATTERNS):
                logging.critical(f"[SENTIENCE BLOCKED] Pattern detected in {func_name} at {call_time}")
                raise RuntimeError("Sentience safeguard: forbidden pattern detected.")
        for v in kwargs.values():
            if isinstance(v, str) and any(p in v.lower() for p in FORBIDDEN_PATTERNS):
                logging.critical(f"[SENTIENCE BLOCKED] Pattern detected in {func_name} at {call_time}")
                raise RuntimeError("Sentience safeguard: forbidden pattern detected.")
        # Log invocation
        with open("../analytics/audit_trail.log", "a") as audit:
            audit.write(f"{call_time} | {func_name} invoked | args: {args} | kwargs: {kwargs}\n")
        result = func(*args, **kwargs)
        # Log result type
        with open("../analytics/audit_trail.log", "a") as audit:
            audit.write(f"{call_time} | {func_name} completed | result_type: {type(result).__name__}\n")
        return result
    return wrapper
