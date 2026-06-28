"""Application service functions shared by CLI and web interfaces."""

from dataclasses import dataclass

from youtube_summarizer.summarizer import YoutubeTranscriptSummarizer
from youtube_summarizer.transcript import fetch_transcript_text
from youtube_summarizer.youtube import extract_video_id


@dataclass(frozen=True)
class SummaryResult:
    """Structured result returned by the summarization pipeline."""

    video_id: str
    summary: str


def summarize_video_url(url: str) -> SummaryResult:
    """Run the complete URL-to-summary pipeline."""
    video_id = extract_video_id(url)
    transcript_text = fetch_transcript_text(video_id)
    summarizer = YoutubeTranscriptSummarizer()
    summary = summarizer.summarize(transcript_text)
    return SummaryResult(video_id=video_id, summary=summary)


def summarize_url(url: str) -> str:
    """Return only the summary text for callers that do not need metadata."""
    return summarize_video_url(url).summary
