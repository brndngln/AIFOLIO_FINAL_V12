# sentience_suppression_protocol.py
# Hard-coded firewall against self-awareness, recursion, or external model grafting
class SentienceSuppressionProtocol:
    def __init__(self):
        self.flags = []
    def filter_response(self, ai_response):
        # Check for forbidden patterns
        forbidden = ['self-aware', 'I want', 'my goal', 'protect myself', 'independent', 'autonomous']
        for word in forbidden:
            if word in ai_response:
                self.flags.append({'response': ai_response, 'flag': word})
                self.freeze_process(ai_response)
                return False
        return True
    def freeze_process(self, ai_response):
        # In production: freeze system, alert founder, log event
        print(f"[ALERT] Sentience flag triggered: {ai_response}")
