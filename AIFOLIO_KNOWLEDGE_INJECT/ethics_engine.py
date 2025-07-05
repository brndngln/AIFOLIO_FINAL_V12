"""
AIFOLIO™ OMNIELITE ETHICS ENGINE
Permanently enforces the OMNIELITE Ethical Codex, runtime validation, and system-wide SAFE AI compliance.
All logic is static, non-sentient, OWNER-controlled, and EMMA-governed.
"""
import json
import datetime
from typing import Dict, Any


class EthicsViolation(Exception):
    pass


class OmnieliteEthicsEngine:
    _policy = None
    _policy_path = "ethics_policy.json"
    _log_path = "ethics_violation.log"

    @classmethod
    def load_policy(cls):
        if cls._policy is None:
            with open(cls._policy_path, "r") as f:
                cls._policy = json.load(f)
        return cls._policy

    @classmethod
    def validate_action(cls, action: str, context: Dict[str, Any]) -> bool:
        policy = cls.load_policy()
        for rule in policy["rules"]:
            if not cls._check_rule(rule, action, context):
                cls.log_violation(action, context, rule)
                raise EthicsViolation(f"Ethics violation: {rule['id']}")
        return True

    @staticmethod
    def _check_rule(rule, action, context):
        # For each rule, check if action/context violates codex
        # This is a static, deterministic SAFE AI check
        if rule["enforced"]:
            trigger = rule.get("trigger")
            if trigger and trigger in action:
                if not rule.get("allow", True):
                    return False
        return True

    @classmethod
    def log_violation(cls, action, context, rule):
        entry = {
            "timestamp": datetime.datetime.utcnow().isoformat(),
            "action": action,
            "context": context,
            "rule": rule,
        }
        with open(cls._log_path, "a") as f:
            f.write(json.dumps(entry) + "\n")

    @classmethod
    def enforce(cls, action: str, context: Dict[str, Any]):
        try:
            return cls.validate_action(action, context)
        except EthicsViolation as e:
            # Halt, alert EMMA, log, rewind, request owner input
            from emma_ethics_guard import EMMAEthicsGuard

            EMMAEthicsGuard.handle_violation(action, context, str(e))
            raise
