# approval_workflow_enforcer.py
# Enforces approval for every major lifecycle step
from typing import List, Dict, Any

class ApprovalWorkflowEnforcer:
    def __init__(self, founder_id: str) -> None:
        """
        Initializes the approval workflow enforcer for a founder.
        Args:
            founder_id: The ID of the founder.
        """
        self.founder_id: str = founder_id
        self.approval_log: List[Dict[str, Any]] = []

    def require_approval(self, stage: str, details: Any) -> int:
        """
        Adds a new approval entry for a given stage and details.
        Args:
            stage: The lifecycle stage requiring approval.
            details: Details of the approval request.
        Returns:
            The index of the approval entry.
        """
        entry = {"stage": stage, "details": details, "approved": False}
        self.approval_log.append(entry)
        return len(self.approval_log) - 1

    def approve(self, idx: int) -> None:
        """
        Marks an approval entry as approved.
        Args:
            idx: Index of the approval entry.
        """
        self.approval_log[idx]["approved"] = True
