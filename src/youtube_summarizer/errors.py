"""Custom exceptions with user-friendly messages."""


class YoutubeSummarizerError(Exception):
    """Base exception for expected application failures."""


class InvalidYoutubeUrlError(YoutubeSummarizerError):
    """Raised when a URL does not contain a supported YouTube video ID."""


class TranscriptFetchError(YoutubeSummarizerError):
    """Raised when a transcript cannot be fetched for the video."""


class SummaryGenerationError(YoutubeSummarizerError):
    """Raised when the language model cannot generate the summary."""
