# goal_priority_matrix.py
# Loads and manages goal funding priorities
import json


class GoalPriorityMatrix:
    def __init__(self, matrix_path="core/goal_priority_matrix.json"):
        with open(matrix_path) as f:
            self.matrix = json.load(f)

    def get_priority(self, goal):
        return self.matrix.get(goal, 0.0)
