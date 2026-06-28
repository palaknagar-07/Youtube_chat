"""Command-line interface."""

from youtube_summarizer.errors import YoutubeSummarizerError
from youtube_summarizer.service import summarize_url


def main() -> int:
    """Prompt for a YouTube URL and print the generated summary."""
    print("YouTube Video Summarizer")
    url = input("Paste YouTube URL: ").strip()

    if not url:
        print("Please paste a YouTube URL.")
        return 1

    try:
        print("\nFetching transcript and generating summary. This can take a moment...\n")
        summary = summarize_url(url)
    except YoutubeSummarizerError as exc:
        print(f"Error: {exc}")
        return 1

    print(summary)
    return 0
