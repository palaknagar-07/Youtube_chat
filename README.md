# YouTube ChatHelp

Terminal-first YouTube video summarizer powered by LangChain and Ollama.

Phase one accepts a YouTube URL, fetches the transcript, splits long transcripts
into chunks, summarizes each chunk with `llama3.2`, and combines those section
summaries into one polished final summary.

## Requirements

- Python 3.10+
- Ollama installed and running
- Llama 3.2 pulled locally

Install the Ollama model:

```bash
ollama pull llama3.2
```

Install Python dependencies:

```bash
pip install -r requirements.txt
```

## Run

```bash
python src/main.py
```

Then paste a YouTube URL when prompted.

## Current Scope

This phase does not use embeddings or a vector database. Embeddings are better
suited for a later "chat with video" feature where the app needs to retrieve
specific transcript sections for user questions. For summarization, the current
pipeline uses transcript text directly.

## Project Structure

```text
src/
  app.ipynb                    Existing notebook, kept untouched
  main.py                      Terminal entry point
  youtube_summarizer/
    cli.py                     Terminal interaction and pipeline entry
    config.py                  Model and chunk settings
    errors.py                  User-friendly exceptions
    prompts.py                 LangChain prompt templates
    summarizer.py              LangChain/Ollama summary pipeline
    transcript.py              YouTube transcript fetching
    youtube.py                 YouTube URL parsing
```
