import json
import datetime
import os

THANKYOU_LOG = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__), "../../analytics/personalized_thankyou_log.jsonl"
    )
)
os.makedirs(os.path.dirname(THANKYOU_LOG), exist_ok=True)

TEMPLATES = [
    "Thank you for your purchase, {name}! Your support means a lot.",
    "Hi {name}, thanks for choosing AIFOLIO™. We hope you love your new vault!",
    "Hello {name}, your order is confirmed. Welcome to the AIFOLIO™ community!",
]


def generate_thankyou(name, template_idx=0):
    template = TEMPLATES[template_idx % len(TEMPLATES)]
    note = template.format(name=name)
    entry = {
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "name": name,
        "template": template,
        "note": note,
    }
    with open(THANKYOU_LOG, "a") as f:
        f.write(json.dumps(entry) + "\n")
    return note


if __name__ == "__main__":
    print(generate_thankyou("Alex"))
