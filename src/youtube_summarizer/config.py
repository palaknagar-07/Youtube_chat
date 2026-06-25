"""Application configuration."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    model_name: str = "llama3.2"
    temperature: float = 0.2
    chunk_size: int = 5000
    chunk_overlap: int = 500
    transcript_languages: tuple[str, ...] = ("en", "en-US", "en-GB", "hi")


settings = Settings()
