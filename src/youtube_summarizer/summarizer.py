"""LangChain/Ollama summarization pipeline."""

from langchain_core.output_parsers import StrOutputParser
from langchain_ollama import ChatOllama
from langchain_text_splitters import RecursiveCharacterTextSplitter

from youtube_summarizer.config import settings
from youtube_summarizer.errors import SummaryGenerationError
from youtube_summarizer.prompts import CHUNK_SUMMARY_PROMPT, FINAL_SUMMARY_PROMPT


class YoutubeTranscriptSummarizer:
    """Summarize transcripts with a chunk-and-combine LangChain pipeline."""

    def __init__(
        self,
        model_name: str = settings.model_name,
        temperature: float = settings.temperature,
        chunk_size: int = settings.chunk_size,
        chunk_overlap: int = settings.chunk_overlap,
    ) -> None:
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", ". ", "? ", "! ", " ", ""],
        )
        self.llm = ChatOllama(model=model_name, temperature=temperature)
        self.chunk_chain = CHUNK_SUMMARY_PROMPT | self.llm | StrOutputParser()
        self.final_chain = FINAL_SUMMARY_PROMPT | self.llm | StrOutputParser()

    def summarize(self, transcript_text: str) -> str:
        """Create a final summary from raw transcript text."""
        chunks = self.splitter.split_text(transcript_text)

        if not chunks:
            raise SummaryGenerationError("The transcript could not be split for summary.")

        try:
            if len(chunks) == 1:
                section_summaries = [
                    self.chunk_chain.invoke({"chunk": chunks[0]}).strip()
                ]
            else:
                section_summaries = [
                    self.chunk_chain.invoke({"chunk": chunk}).strip()
                    for chunk in chunks
                ]

            combined = "\n\n".join(
                f"Section {index}:\n{summary}"
                for index, summary in enumerate(section_summaries, start=1)
            )
            return self.final_chain.invoke({"summaries": combined}).strip()
        except Exception as exc:
            raise SummaryGenerationError(
                "Ollama could not generate the summary. Make sure Ollama is running "
                "and the llama3.2 model is installed."
            ) from exc
