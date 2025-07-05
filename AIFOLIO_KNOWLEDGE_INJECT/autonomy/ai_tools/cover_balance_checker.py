import json
import datetime
import os
from PIL import Image, ImageStat

COVER_LOG = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__), "../../analytics/cover_balance_checker_log.jsonl"
    )
)
os.makedirs(os.path.dirname(COVER_LOG), exist_ok=True)


# --- AI Static Cover Balance Checker ---
def check_cover_balance(image_path):
    try:
        img = Image.open(image_path).convert("L")
        stat = ImageStat.Stat(img)
        mean = stat.mean[0]
        stddev = stat.stddev[0]
        balance_score = 1 - abs(mean - 128) / 128  # 0=unbalanced, 1=perfectly balanced
        result = {"mean": mean, "stddev": stddev, "balance_score": balance_score}
        status = "ok"
    except Exception as e:
        result = {"error": str(e)}
        status = "error"
    entry = {
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "image_path": image_path,
        "result": result,
        "status": status,
    }
    with open(COVER_LOG, "a") as f:
        f.write(json.dumps(entry) + "\n")
    return result
