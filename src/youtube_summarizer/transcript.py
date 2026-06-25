"""Transcript loading and formatting."""

from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import (
    CouldNotRetrieveTranscript,
    NoTranscriptFound,
    TranscriptsDisabled,
    VideoUnavailable,
)

from youtube_summarizer.config import settings
from youtube_summarizer.errors import TranscriptFetchError


def fetch_transcript_text(
    video_id: str,
    languages: tuple[str, ...] = settings.transcript_languages,
) -> str:
    """Fetch and flatten the transcript text for a YouTube video."""
    try:
        transcript = YouTubeTranscriptApi().fetch(video_id, languages=list(languages))
    except (NoTranscriptFound, TranscriptsDisabled, VideoUnavailable) as exc:
        raise TranscriptFetchError(
            "I could not fetch a transcript for this video. It may be disabled, "
            "private, unavailable, or missing the requested language transcript."
        ) from exc
    except CouldNotRetrieveTranscript as exc:
        raise TranscriptFetchError(
            "YouTube did not return a usable transcript for this video."
        ) from exc
    except Exception as exc:
        raise TranscriptFetchError(
            "Something went wrong while fetching the YouTube transcript."
        ) from exc

    text = " ".join(snippet.text.replace("\n", " ").strip() for snippet in transcript)
    normalized = " ".join(text.split())

    if not normalized:
        raise TranscriptFetchError("The fetched transcript was empty.")

    return normalized
