import json
import datetime
import os

OWNER_LOCK = True
import random

RANDOMIZER_LOG = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__), "../../analytics/safe_ai_randomizer_log.jsonl"
    )
)
os.makedirs(os.path.dirname(RANDOMIZER_LOG), exist_ok=True)

STYLE_SHIFTS = [
    lambda t: t.replace("Thank you", "We appreciate"),
    lambda t: t.replace("Best regards", "Warm wishes"),
    lambda t: t.replace("Hi", "Hello"),
    lambda t: t + " Have a great day!",
]


def safe_randomize(text: str) -> str:
    """
    Applies a minor, brand-safe style shift. Human preview required for all outputs.
    """
    shift = random.choice(STYLE_SHIFTS)
    randomized = shift(text)
    entry = {
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "original": text,
        "randomized": randomized,
        "human_approval_required": True,
    }
    with open(RANDOMIZER_LOG, "a") as f:
        f.write(json.dumps(entry) + "\n")
    return randomized


if __name__ == "__main__":
    print(safe_randomize("Thank you for your purchase! Best regards,"))
