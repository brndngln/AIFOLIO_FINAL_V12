# WIND_PLACEHOLDER
def ensure_utf8(file_path):
    with open(file_path, "rb") as f:
        raw = f.read()
    try:
        raw.decode("utf-8")
        return True
    except UnicodeDecodeError:
        return False
