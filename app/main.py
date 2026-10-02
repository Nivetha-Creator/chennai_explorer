from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.api.chat import router as chat_router


BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"


app = FastAPI(
    title="Chennai Explorer",
    description="AI-powered Chennai travel and exploration assistant",
    version="1.0.0",
)


# Serve frontend files
app.mount(
    "/frontend",
    StaticFiles(directory=FRONTEND_DIR),
    name="frontend",
)


# API routes
app.include_router(chat_router)


@app.get("/")
async def home():

    return FileResponse(
        FRONTEND_DIR / "index.html"
    )


@app.get("/api/health")
async def health_check():

    return {
        "status": "online",
        "app": "Chennai Explorer",
    }