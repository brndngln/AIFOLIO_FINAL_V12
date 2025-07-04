"""
AIFOLIO™ Private Entrypoint
Owner-locked admin access. No public endpoints.
"""
import os
import sys
from dotenv import load_dotenv

load_dotenv()

ADMIN_KEY = os.getenv("AIFOLIO_ADMIN_KEY")

if not ADMIN_KEY:
    print("[SECURITY ERROR] Admin key not set in .env. Exiting.")
    sys.exit(1)

def check_admin_key(input_key):
    """Verify admin key for all access. No public login/signup."""
    return input_key == ADMIN_KEY

# Example usage: prompt for admin key on CLI (replace with UI as needed)
if __name__ == "__main__":
    input_key = input("Enter admin key: ")
    if not check_admin_key(input_key):
        print("[ACCESS DENIED] Invalid admin key.")
        sys.exit(1)
    print("[ACCESS GRANTED] Welcome, owner.")
    # Proceed to dashboard/main app
