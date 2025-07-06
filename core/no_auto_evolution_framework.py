# no_auto_evolution_framework.py
# Prevents self-rewrite or logic mutation unless founder commands
class NoAutoEvolutionFramework:
    def __init__(self, founder_key: str) -> None:
        self.founder_key: str = founder_key

    def permit_change(self, request: str, key: str) -> bool:
        return key == self.founder_key
