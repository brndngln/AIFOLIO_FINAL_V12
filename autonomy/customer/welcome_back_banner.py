import json
import datetime
import os

BANNER_LOG = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../analytics/welcome_back_log.jsonl'))
os.makedirs(os.path.dirname(BANNER_LOG), exist_ok=True)

BANNERS = [
    "Welcome back, {name}! Ready for your next vault?",
    "Hi {name}, great to see you again! Check out what's new.",
    "Hello {name}, your loyalty is awesome. Enjoy exclusive bonuses!"
]

def get_welcome_back_banner(name, banner_idx=0):
    banner = BANNERS[banner_idx % len(BANNERS)].format(name=name)
    entry = {
        'timestamp': datetime.datetime.utcnow().isoformat() + 'Z',
        'name': name,
        'banner': banner
    }
    with open(BANNER_LOG, 'a') as f:
        f.write(json.dumps(entry) + '\n')
    return banner

if __name__ == "__main__":
    print(get_welcome_back_banner('Alex'))
