#=============================================================================
#=============================================================================
#Title: Data Collection and Analytics
#Course: COSC 381 - Software Engineering Solutions
#Description:
#File: app.py
#Revision: 1
#Revision Date: 09/14/2026
#Project Files:
#   /app.py
#   /templates/index.html
#   /static/app.css
#   /static/app.js
#=============================================================================
#=============================================================================

# ---------------------------------------------------------------------------
# Library imports
# ---------------------------------------------------------------------------

from contextlib import asynccontextmanager
from pathlib import Path
import uvicorn
import aiosqlite
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Application paths
# ---------------------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
DB_FILE = BASE_DIR / "app_data.db"
STATIC_DIR = BASE_DIR / "static"
TEMPLATES_DIR = BASE_DIR / "templates"

# ---------------------------------------------------------------------------
# Database initialization
# ---------------------------------------------------------------------------

async def init_db() -> None:

    async with aiosqlite.connect(DB_FILE) as db:
        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL
            )
            """
        )
        await db.commit()

    print(f"Database initialized: {DB_FILE}")

# ---------------------------------------------------------------------------
# FastAPI lifespan
# ---------------------------------------------------------------------------

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting Data Collection and Analytics")
    print(f"Application directory: {BASE_DIR}")
    print(f"Database file: {DB_FILE}")

    await init_db()

    yield

    print("Stopping application")


# ---------------------------------------------------------------------------
# FastAPI application
# ---------------------------------------------------------------------------

app = FastAPI(
    title="Data Collection and Analytics",
    description="",
    version="1.0.0",
    lifespan=lifespan,
)

# ---------------------------------------------------------------------------
# Static files and templates
# ---------------------------------------------------------------------------

app.mount(
    "/static",
    StaticFiles(directory=str(STATIC_DIR)),
    name="static",
)

templates = Jinja2Templates(
    directory=str(TEMPLATES_DIR)
)


# ---------------------------------------------------------------------------
# Web page
# ---------------------------------------------------------------------------

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={},
    )


# ---------------------------------------------------------------------------
# API endpoints
# ---------------------------------------------------------------------------

@app.get("/app", response_class=HTMLResponse)
async def app_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="app.html",
        context={}
    )

    
if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
    )
