# approval_workflow_enforcer.py
# Enforces approval for every major lifecycle step
class ApprovalWorkflowEnforcer:
    def __init__(self, founder_id):
        self.founder_id = founder_id
        self.approval_log = []

    def require_approval(self, stage, details):
        entry = {"stage": stage, "details": details, "approved": False}
        self.approval_log.append(entry)
        return len(self.approval_log) - 1

    def approve(self, idx):
        self.approval_log[idx]["approved"] = True
