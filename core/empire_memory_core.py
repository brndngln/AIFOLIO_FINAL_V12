# empire_memory_core.py — OMNIELITE V3: Persistent intelligence memory
import json


class EmpireMemoryCore:
    def __init__(self, path="core/empire_memory_core.json"):
        self.path = path
        self.memory = {}

    def load(self):
        with open(self.path, "r") as f:
            self.memory = json.load(f)

    def save(self):
        with open(self.path, "w") as f:
            json.dump(self.memory, f, indent=2)
