import os
from dotenv import load_dotenv

load_dotenv()

def require(name):
    value = os.getenv(name)
    if not value:
        raise ValueError(f"Missing required environment variable: {name}")
    return value

DATABASE_URL = require("DATABASE_URL")
SUPABASE_URL = require("SUPABASE_URL")
SUPABASE_KEY = require("SUPABASE_KEY")
PORT = int(os.getenv("PORT", "8000"))
PUBLIC_BASE_URL = os.getenv("PUBLIC_BASE_URL", "http://localhost:8000")