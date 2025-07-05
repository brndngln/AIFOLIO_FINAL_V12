"""
AIFOLIO™ Viral Reward Protocol
Social sharing = credits, vault unlocks, or private drops. SAFE AI: static, deterministic, owner-controlled.
"""
import logging

STATIC_REWARDS = [
    {"action": "share", "reward": "5 credits"},
    {"action": "invite", "reward": "private drop"},
    {"action": "review", "reward": "vault unlock"},
]


def get_viral_reward(action):
    for reward in STATIC_REWARDS:
        if reward["action"] == action:
            logging.info(
                f"Viral Reward Protocol: Action {action}, Reward: {reward['reward']}"
            )
            return reward
    return None
