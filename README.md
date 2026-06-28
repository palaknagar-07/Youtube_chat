# YouTube ChatHelp

Local YouTube video summarizer powered by LangChain, Ollama, and FastAPI.

The app accepts a YouTube URL, fetches the transcript, splits long transcripts
into chunks, summarizes each chunk with `llama3.2`, and combines those section
summaries into one polished final summary.

It now includes a minimal local web UI served by FastAPI.

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
./venv/bin/python -m pip install -r requirements.txt
```

## Run Web App

Start Ollama first, then run:

```bash
./venv/bin/python -m uvicorn api.main:app --reload
```

Open:

```text
http://127.0.0.1:8000
```

FastAPI docs are available at:

```text
http://127.0.0.1:8000/docs
```

## Run Terminal App

```bash
./venv/bin/python src/main.py
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
    service.py                 Shared app service used by CLI and API
    summarizer.py              LangChain/Ollama summary pipeline
    transcript.py              YouTube transcript fetching
    youtube.py                 YouTube URL parsing
api/
  main.py                      FastAPI app and JSON endpoints
web/
  index.html                   Minimal local UI
  static/
    app.js                     Browser behavior and API calls
    styles.css                 UI styling
```
