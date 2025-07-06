# legal_action_gatekeeper.py
# No legal change unless proposed and digitally approved
class LegalActionGatekeeper:
    def __init__(self) -> None:
        self.pending: list[dict[str, object]] = []

    def propose_action(self, summary: str) -> int:
        self.pending.append({"summary": summary, "approved": False})
        return len(self.pending) - 1

    def approve(self, idx: int) -> None:
        self.pending[idx]["approved"] = True
