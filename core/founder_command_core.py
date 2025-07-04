# founder_command_core.py
# All critical actions must pass through the Founder Command Console (FCC)
class FounderCommandCore:
    def __init__(self, founder_id):
        self.founder_id = founder_id
        self.log = []
    def request_approval(self, action, impact, risks, ai_reasoning):
        report = {
            'action': action,
            'impact': impact,
            'risks': risks,
            'ai_reasoning': ai_reasoning,
            'status': 'pending',
            'decision': None
        }
        self.log.append(report)
        # In production: send to dashboard, push, and email for approval
        return report
    def record_decision(self, report_idx, decision):
        self.log[report_idx]['decision'] = decision
        self.log[report_idx]['status'] = 'approved' if decision == 'approve' else 'denied'
