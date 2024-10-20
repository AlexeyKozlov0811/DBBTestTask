import os

from dotenv import load_dotenv

# Connect the path with your '.env' file name
load_dotenv('.env')

SECRET_KEY = os.getenv("SECRET_KEY", "<change-me>")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# to allow incorrect ISBN for testing
SKIP_ISBN_CHECKSUM_VALIDATION = True

# user settings
BORROWING_DAYS = 30
