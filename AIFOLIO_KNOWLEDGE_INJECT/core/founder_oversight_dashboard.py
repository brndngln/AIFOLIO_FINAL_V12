# founder_oversight_dashboard.py
# Real-time logging and CEO review for all actions
class FounderOversightDashboard:
    def __init__(self):
        self.action_log = []

    def log_action(self, who, what, when, why, needs_review=False):
        entry = {
            "who": who,
            "what": what,
            "when": when,
            "why": why,
            "needs_review": needs_review,
        }
        self.action_log.append(entry)

    def get_review_queue(self):
        return [a for a in self.action_log if a["needs_review"]]
