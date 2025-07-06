# goal_priority_matrix.py
# Loads and manages goal funding priorities
import json
from typing import Dict, Any


class GoalPriorityMatrix:
    def __init__(self, matrix_path: str = "core/goal_priority_matrix.json") -> None:
        with open(matrix_path) as f:
            self.matrix: Dict[str, float] = json.load(f)

    def get_priority(self, goal: str) -> float:
        return self.matrix.get(goal, 0.0)
