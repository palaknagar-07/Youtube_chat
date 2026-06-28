const form = document.querySelector("#summary-form");
const urlInput = document.querySelector("#youtube-url");
const submitButton = document.querySelector("#submit-button");
const message = document.querySelector("#message");
const summaryPanel = document.querySelector("#summary-panel");
const summaryMeta = document.querySelector("#summary-meta");
const summary = document.querySelector("#summary");
const resultActions = document.querySelector("#result-actions");
const copyButton = document.querySelector("#copy-button");
const clearButton = document.querySelector("#clear-button");
const healthStatus = document.querySelector("#health-status");

let latestSummary = "";

function setMessage(text, type = "info") {
  message.textContent = text;
  message.className = `message${type === "error" ? " error" : ""}`;
  message.hidden = false;
}

function clearMessage() {
  message.hidden = true;
  message.textContent = "";
  message.className = "message";
}

function setLoading(isLoading) {
  submitButton.disabled = isLoading;
  urlInput.disabled = isLoading;
  submitButton.textContent = isLoading ? "Summarizing..." : "Summarize";
}

function escapeHtml(value) {
  return value
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function renderMarkdown(markdown) {
  const lines = markdown.split(/\r?\n/);
  const html = [];
  let inList = false;

  function closeList() {
    if (inList) {
      html.push("</ul>");
      inList = false;
    }
  }

  for (const line of lines) {
    const trimmed = line.trim();

    if (!trimmed) {
      closeList();
      continue;
    }

    if (trimmed.startsWith("### ")) {
      closeList();
      html.push(`<h3>${escapeHtml(trimmed.slice(4))}</h3>`);
      continue;
    }

    if (trimmed.startsWith("## ")) {
      closeList();
      html.push(`<h2>${escapeHtml(trimmed.slice(3))}</h2>`);
      continue;
    }

    if (trimmed.startsWith("# ")) {
      closeList();
      html.push(`<h1>${escapeHtml(trimmed.slice(2))}</h1>`);
      continue;
    }

    if (trimmed.startsWith("- ")) {
      if (!inList) {
        html.push("<ul>");
        inList = true;
      }
      html.push(`<li>${escapeHtml(trimmed.slice(2))}</li>`);
      continue;
    }

    closeList();
    html.push(`<p>${escapeHtml(trimmed)}</p>`);
  }

  closeList();
  return html.join("");
}

async function loadHealth() {
  try {
    const response = await fetch("/api/health");
    if (!response.ok) {
      throw new Error("Backend unavailable");
    }
    const data = await response.json();
    healthStatus.textContent = `Backend ready · ${data.model}`;
    healthStatus.classList.add("ok");
  } catch {
    healthStatus.textContent = "Backend unavailable";
    healthStatus.classList.remove("ok");
  }
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();

  const url = urlInput.value.trim();
  if (!url) {
    setMessage("Please paste a YouTube URL.", "error");
    return;
  }

  clearMessage();
  setLoading(true);
  setMessage("Fetching transcript and asking your local Ollama model...");

  try {
    const response = await fetch("/api/summarize", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ url }),
    });

    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.detail || "Something went wrong.");
    }

    latestSummary = data.summary;
    summaryMeta.textContent = `Video ID: ${data.video_id}`;
    summary.innerHTML = renderMarkdown(data.summary);
    summaryPanel.hidden = false;
    resultActions.hidden = false;
    clearMessage();
  } catch (error) {
    setMessage(error.message, "error");
  } finally {
    setLoading(false);
  }
});

copyButton.addEventListener("click", async () => {
  if (!latestSummary) {
    return;
  }

  await navigator.clipboard.writeText(latestSummary);
  copyButton.textContent = "Copied";
  setTimeout(() => {
    copyButton.textContent = "Copy";
  }, 1400);
});

clearButton.addEventListener("click", () => {
  latestSummary = "";
  urlInput.value = "";
  summary.innerHTML = "";
  summaryMeta.textContent = "";
  summaryPanel.hidden = true;
  resultActions.hidden = true;
  clearMessage();
  urlInput.focus();
});

loadHealth();
