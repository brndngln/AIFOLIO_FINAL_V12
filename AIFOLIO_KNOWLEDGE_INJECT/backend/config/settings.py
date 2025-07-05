import os

# Centralized settings for backend authentication and JWT
SECRET_USERNAME = os.getenv("AIFOLIO_USER", "aifolio_owner")
SECRET_KEY = os.getenv("AIFOLIO_JWT_SECRET", "supersecretjwtkey")
ALGORITHM = "HS256"
