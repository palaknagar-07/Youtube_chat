"""FastAPI backend for the local YouTube ChatHelp web UI."""

from pathlib import Path
import sys

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from starlette.concurrency import run_in_threadpool


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
WEB_DIR = PROJECT_ROOT / "web"
STATIC_DIR = WEB_DIR / "static"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from youtube_summarizer.config import settings  # noqa: E402
from youtube_summarizer.errors import (  # noqa: E402
    InvalidYoutubeUrlError,
    SummaryGenerationError,
    TranscriptFetchError,
    YoutubeSummarizerError,
)
from youtube_summarizer.service import summarize_video_url  # noqa: E402


class SummarizeRequest(BaseModel):
    """Request body for a summary generation call."""

    url: str


class SummarizeResponse(BaseModel):
    """Successful summary response."""

    status: str
    video_id: str
    summary: str


app = FastAPI(title="YouTube ChatHelp", version="0.1.0")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/")
def index() -> FileResponse:
    """Serve the local web UI."""
    return FileResponse(WEB_DIR / "index.html")


@app.get("/api/health")
def health() -> dict[str, str | float]:
    """Return basic backend configuration for the UI."""
    return {
        "status": "ok",
        "model": settings.model_name,
        "temperature": settings.temperature,
    }


@app.post("/api/summarize", response_model=SummarizeResponse)
async def summarize(request: SummarizeRequest) -> SummarizeResponse:
    """Generate a summary for a YouTube URL using the local Ollama model."""
    url = request.url.strip()
    if not url:
        raise HTTPException(status_code=400, detail="Please paste a YouTube URL.")

    try:
        result = await run_in_threadpool(summarize_video_url, url)
    except InvalidYoutubeUrlError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except TranscriptFetchError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except SummaryGenerationError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except YoutubeSummarizerError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return SummarizeResponse(
        status="completed",
        video_id=result.video_id,
        summary=result.summary,
    )
