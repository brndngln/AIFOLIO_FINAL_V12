# legal_action_gatekeeper.py
# No legal change unless proposed and digitally approved
class LegalActionGatekeeper:
    def __init__(self):
        self.pending = []

    def propose_action(self, summary):
        self.pending.append({"summary": summary, "approved": False})
        return len(self.pending) - 1

    def approve(self, idx):
        self.pending[idx]["approved"] = True
