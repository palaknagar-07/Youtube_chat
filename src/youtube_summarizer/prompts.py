"""LangChain prompt templates for summarization."""

from langchain_core.prompts import ChatPromptTemplate


CHUNK_SUMMARY_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You summarize YouTube transcript sections accurately. "
            "Keep facts grounded in the transcript. Preserve important names, "
            "steps, advice, examples, and conclusions. If the transcript is "
            "Hindi or Hinglish, summarize in clear English unless terms are "
            "better kept as-is.",
        ),
        (
            "human",
            """Summarize this transcript section.

Return:
- Main idea
- Important details
- Concrete advice or takeaways
- Any notable examples, names, tools, or numbers

Transcript section:
{chunk}
""",
        ),
    ]
)


FINAL_SUMMARY_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You create polished, useful summaries from YouTube videos. "
            "Use only the provided section summaries. Do not invent facts.",
        ),
        (
            "human",
            """Create a final summary from these section summaries.

Make the output clear, practical, and well structured.

Use this format exactly:

# Video Summary

## Short Summary
Write 3-5 sentences.

## Detailed Summary
Write a coherent explanation of the full video.

## Key Points
- Include the most important ideas.

## Actionable Takeaways
- Include practical steps the viewer can apply.

## Important Topics Mentioned
- Mention names, tools, skills, companies, frameworks, or themes if present.

Section summaries:
{summaries}
""",
        ),
    ]
)
