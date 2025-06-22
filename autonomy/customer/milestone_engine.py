import json
import datetime
import os

MILESTONE_LOG = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../analytics/milestone_log.jsonl'))
os.makedirs(os.path.dirname(MILESTONE_LOG), exist_ok=True)

MILESTONES = [
    (1, "First Purchase! 🎉"),
    (5, "5 Vaults Unlocked! 🏅"),
    (10, "10+ Vaults! You're a Power User! 🚀")
]

def check_milestones(purchase_count):
    achieved = [desc for count, desc in MILESTONES if purchase_count >= count]
    entry = {
        'timestamp': datetime.datetime.utcnow().isoformat() + 'Z',
        'purchase_count': purchase_count,
        'achieved': achieved
    }
    with open(MILESTONE_LOG, 'a') as f:
        f.write(json.dumps(entry) + '\n')
    return achieved

if __name__ == "__main__":
    print(check_milestones(7))
