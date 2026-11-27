from fastapi import FastAPI

from app import config # noqa: F401
from app.routes import health, me, widgets

app = FastAPI(title="Widget & Lead-Capture Platform")

app.include_router(health.router)   
app.include_router(me.router)
app.include_router(widgets.router)
