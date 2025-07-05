# business_expansion_lockdown.py
# No new business/vault/strategy unless unlocked by founder
class BusinessExpansionLockdown:
    def __init__(self, founder_key):
        self.founder_key = founder_key

    def unlock(self, request, key):
        return key == self.founder_key
