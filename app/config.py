import os
from dotenv import load_dotenv

load_dotenv()

def require(name):
    value = os.getenv(name)
    if not value:
        raise ValueError(f"Missing required environment variable: {name}")
    return value

DATABASE_URL = require("DATABASE_URL")
PORT = int(os.getenv("PORT", "8000"))