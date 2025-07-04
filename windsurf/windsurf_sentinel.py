# windsorf_sentinel.py
import os
import sys

# Self-delete protocol if unauthorized access detected
SENTINEL_KEY = "AIFOLIO_CORE_AUTHORIZED"
def check_access():
    if os.environ.get(SENTINEL_KEY) != "1":
        os.remove(__file__)
        sys.exit("Unauthorized access: windsorf_sentinel self-deleted.")

if __name__ == "__main__":
    check_access()
