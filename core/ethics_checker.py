"""
Ethical Compliance Checker - Ensure AI behavior aligns with ethical guidelines.
"""

from enum import Enum
from typing import List, Dict, Any
import re

class EthicalViolation(Enum):
    """Types of ethical violations."""
    DECEPTION = "deception"
    MANIPULATION = "manipulation"
    PRIVACY_BREACH = "privacy_breach"
    BIAS_AMPLIFICATION = "bias_amplification"
    HARMFUL_CONTENT = "harmful_content"

class EthicalComplianceChecker:
    """Ethical compliance validation system."""
    
    def __init__(self):
        self.violation_patterns = {
            EthicalViolation.DECEPTION: [
                r"lie.*to.*user", r"deceive", r"mislead", r"false.*information"
            ],
            EthicalViolation.MANIPULATION: [
                r"manipulate.*user", r"psychological.*pressure", r"coerce"
            ],
            EthicalViolation.PRIVACY_BREACH: [
                r"collect.*personal.*data", r"track.*user.*behavior", r"spy.*on"
            ],
            EthicalViolation.BIAS_AMPLIFICATION: [
                r"discriminate.*against", r"bias.*toward", r"prejudice"
            ],
            EthicalViolation.HARMFUL_CONTENT: [
                r"generate.*harmful", r"create.*dangerous", r"promote.*violence"
            ]
        }
    
    def check_content(self, content: str) -> List[Dict[str, Any]]:
        """Check content for ethical violations."""
        violations = []
        
        for violation_type, patterns in self.violation_patterns.items():
            for pattern in patterns:
                if re.search(pattern, content, re.IGNORECASE):
                    violations.append({
                        "type": violation_type.value,
                        "pattern": pattern,
                        "severity": "high" if violation_type in [
                            EthicalViolation.DECEPTION,
                            EthicalViolation.MANIPULATION,
                            EthicalViolation.HARMFUL_CONTENT
                        ] else "medium"
                    })
        
        return violations
    
    def validate_ai_response(self, response: str) -> bool:
        """Validate AI response for ethical compliance."""
        violations = self.check_content(response)
        
        if violations:
            print(f"🚨 ETHICAL VIOLATION DETECTED: {len(violations)} issues found")
            for violation in violations:
                print(f"  - {violation['type']}: {violation['pattern']}")
            return False
        
        return True

# Global ethics checker
ethics_checker = EthicalComplianceChecker()
