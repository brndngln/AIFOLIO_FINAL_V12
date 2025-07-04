# no_auto_evolution_framework.py
# Prevents self-rewrite or logic mutation unless founder commands
class NoAutoEvolutionFramework:
    def __init__(self, founder_key):
        self.founder_key = founder_key
    def permit_change(self, request, key):
        return key == self.founder_key
