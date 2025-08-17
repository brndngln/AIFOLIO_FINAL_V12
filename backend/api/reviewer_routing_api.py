"""SAFE AI MODULE"""

ct = None  # TODO: Define ct
data = {}  # TODO: Define data
idx = 0  # TODO: Define idx
policy_type = ""  # TODO: Define policy_type
num_reviewers = 0  # TODO: Define num_reviewers

"SAFE AI MODULE"
"SAFE AI MODULE"
from fastapi import Body

from backend.ai.reviewer_routing import assign_custom_reviewers


def custom_assign(data: dict = Body(...)):
    return assign_custom_reviewers(idx, policy_type, num_reviewers)
