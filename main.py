from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.core.database import init_db
from app.routers import employees, properties

# ---------------------------------------------------------------------------
# App instance
# ---------------------------------------------------------------------------
app = FastAPI(
    title="SkyKeysProperties",
    description="Luxury real estate platform for Dubai, Abu Dhabi, and Sharjah.",
    version="1.0.0",
)

# ---------------------------------------------------------------------------
# Static files & templates (used by Jinja2 page routes added later)
# ---------------------------------------------------------------------------
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# ---------------------------------------------------------------------------
# API routers
# ---------------------------------------------------------------------------
app.include_router(employees.router, prefix="/api")
app.include_router(properties.router, prefix="/api")


# ---------------------------------------------------------------------------
# Startup initialization
# ---------------------------------------------------------------------------
@app.on_event("startup")
async def on_startup():
    try:
        init_db()
    except Exception as exc:
        import logging
        logging.error("Database initialization failed: %s", exc)
        raise


# ---------------------------------------------------------------------------
# Health check
# ---------------------------------------------------------------------------
@app.get("/health", tags=["Health"])
def health():
    return {"status": "ok"}
