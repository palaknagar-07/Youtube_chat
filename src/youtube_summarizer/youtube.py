"""YouTube URL helpers."""

from urllib.parse import parse_qs, urlparse

from youtube_summarizer.errors import InvalidYoutubeUrlError


def extract_video_id(url: str) -> str:
    """Extract a YouTube video ID from common YouTube URL formats."""
    parsed_url = urlparse(url.strip())
    hostname = (parsed_url.hostname or "").lower()
    path_parts = [part for part in parsed_url.path.split("/") if part]

    if hostname in {"youtube.com", "www.youtube.com", "m.youtube.com"}:
        if parsed_url.path == "/watch":
            video_id = parse_qs(parsed_url.query).get("v", [None])[0]
            if video_id:
                return video_id

        if path_parts and path_parts[0] in {"shorts", "embed", "live"}:
            if len(path_parts) > 1:
                return path_parts[1]

    if hostname in {"youtu.be", "www.youtu.be"} and path_parts:
        return path_parts[0]

    raise InvalidYoutubeUrlError(
        "I could not find a valid YouTube video ID in that URL."
    )
