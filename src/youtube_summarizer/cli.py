"""Command-line interface."""

from youtube_summarizer.errors import YoutubeSummarizerError
from youtube_summarizer.summarizer import YoutubeTranscriptSummarizer
from youtube_summarizer.transcript import fetch_transcript_text
from youtube_summarizer.youtube import extract_video_id


def summarize_url(url: str) -> str:
    """Run the complete URL-to-summary pipeline."""
    video_id = extract_video_id(url)
    transcript_text = fetch_transcript_text(video_id)
    summarizer = YoutubeTranscriptSummarizer()
    return summarizer.summarize(transcript_text)


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
