# AI Research Assistant

A local multi-agent research system that searches the web, analyzes sources, generates structured reports, verifies claims, and automatically revises the report when necessary.

Built with **LangGraph, LangChain, Ollama, and Qwen3**.

## Overview

AI Research Assistant uses multiple specialized AI agents instead of relying on a single LLM call.

The system follows a complete research workflow:

```text
User Query
    ↓
Researcher Agent
    ↓
Web Search & Source Selection
    ↓
Web Page Reading
    ↓
Analyst Agent
    ↓
Writer Agent
    ↓
Verifier Agent
    ↓
Revision if Needed
    ↓
Final Research Report
```

## Features

- Multi-agent workflow with LangGraph
- Local LLM execution with Ollama
- Web search with DDGS
- Real web page content extraction
- Basic source quality scoring
- Researcher, Analyst, Writer and Verifier agents
- Source-based citations
- Automatic report verification
- Automatic revision loop
- Human-review status for unresolved verification issues
- Markdown report generation
- Research history logging
- Research duration and source tracking
- Configurable project settings
- Ollama and model availability checks
- Basic error handling

## Agents

**Researcher Agent**  
Searches the web, selects sources, reads web pages and prepares source-based research notes.

**Analyst Agent**  
Compares the collected information, identifies key findings and prepares a structured analysis.

**Writer Agent**  
Transforms the analysis into a readable research report with citations and references.

**Verifier Agent**  
Checks whether claims, dates, statistics and citations are supported by the collected sources.

If problems are detected, the report is automatically sent back to the Writer Agent for revision.

## Tech Stack

- Python
- LangGraph
- LangChain
- Ollama
- Qwen3 4B Instruct
- DDGS
- BeautifulSoup
- Requests

## Project Structure

```text
ai-research-assistant/
│
├── agents/
│   ├── researcher.py
│   ├── analyst.py
│   ├── writer.py
│   └── verifier.py
│
├── utils/
│   ├── web_search.py
│   ├── page_reader.py
│   ├── report_saver.py
│   └── system_check.py
│
├── config.py
├── settings.py
├── state.py
├── main.py
├── requirements.txt
└── README.md
```

## How It Works

1. The user enters a research topic.
2. The Researcher Agent searches the web.
3. Sources are ranked and selected.
4. Relevant content is extracted from selected web pages.
5. The Analyst Agent analyzes the collected information.
6. The Writer Agent creates a structured report.
7. The Verifier Agent checks the report against the sources.
8. If necessary, the report is automatically revised once.
9. The final report is saved locally as a Markdown file.

## Local LLM

The project uses Ollama to run the language model locally.

Current model:

```text
qwen3:4b-instruct
```

No OpenAI API key is required.

> The language model runs locally, but web searches and public web page requests still require an internet connection.

## Installation

Clone the repository:

```bash
git clone YOUR_REPOSITORY_URL
cd ai-research-assistant
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Install Ollama and download the model:

```bash
ollama pull qwen3:4b-instruct
```

## Usage

Run:

```bash
python main.py
```

Then enter a research topic:

```text
Araştırmak istediğiniz konuyu yazın:
```

Example:

```text
Yapay zekanın yazılım geliştirmede kullanım alanları
```

## Output

Generated reports are saved under:

```text
outputs/reports/
```

Research execution history is stored in:

```text
outputs/history.jsonl
```

The `outputs/` directory is excluded from Git tracking.

At the end of a research session, the system can display information such as:

```text
Yapılan otomatik düzeltme sayısı: 1
Kullanılan kaynak sayısı: 3
Toplam araştırma süresi: 120.45 saniye
Son durum: DOĞRULANDI
```

If verification problems remain after the allowed revision:

```text
Son durum: İNSAN İNCELEMESİ GEREKLİ
```

## Configuration

Main settings can be changed from `settings.py`.

Examples include:

```python
MODEL_NAME = "qwen3:4b-instruct"
SEARCH_RESULT_COUNT = 3
PAGE_MAX_CHARS = 1000
MAX_REVISIONS = 1
MODEL_TEMPERATURE = 0
MODEL_MAX_OUTPUT_TOKENS = 300
```

## Limitations

- Source ranking is heuristic-based.
- Some websites may block automated access.
- JavaScript-heavy pages may not be fully readable.
- The Verifier Agent is also an LLM and can make mistakes.
- Local inference speed depends on the computer's hardware.
- Important research results should still be reviewed by a human.

## Future Improvements

- RAG and vector database support
- PDF and academic paper research
- Improved citation validation
- Parallel agent execution
- Streamlit or Gradio interface
- PDF/DOCX export
- Automated tests
- Docker support

## Disclaimer

This project is an experimental AI research assistant. Generated information and automated verification results should not be treated as guaranteed factual correctness.