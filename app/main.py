from fastapi import FastAPI

from app import config # noqa: F401
from app.routes import health

app = FastAPI(title="Widget & Lead-Capture Platform")

app.include_router(health.router)   