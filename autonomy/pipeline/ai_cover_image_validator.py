import os
import json
import datetime
from PIL import Image

COVER_LOG = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__), "../../analytics/ai_cover_image_validator_log.jsonl"
    )
)
os.makedirs(os.path.dirname(COVER_LOG), exist_ok=True)


# --- Cover Image Validator ---
def validate_cover_image(image_path):
    result = {
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "image_path": image_path,
        "legible": False,
        "brand_consistent": False,
        "inappropriate": False,
        "human_preview_required": True,
    }
    if not os.path.exists(image_path):
        result["error"] = "file_not_found"
        with open(COVER_LOG, "a") as f:
            f.write(json.dumps(result) + "\n")
        return result
    try:
        img = Image.open(image_path)
        # Legibility: check contrast (stub: mean pixel value)
        gray = img.convert("L")
        mean = sum(gray.getdata()) / (gray.width * gray.height)
        result["legible"] = mean > 40 and mean < 215
        # Brand consistency (stub: require certain color range)
        # (In production, check for logo, palette, etc.)
        result["brand_consistent"] = True  # Placeholder
        # Inappropriate imagery (stub: flag if too dark/bright)
        result["inappropriate"] = mean < 20 or mean > 235
    except Exception as e:
        result["error"] = str(e)
    with open(COVER_LOG, "a") as f:
        f.write(json.dumps(result) + "\n")
    return result


if __name__ == "__main__":
    print(validate_cover_image("cover.jpg"))
