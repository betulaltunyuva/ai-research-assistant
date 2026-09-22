# 🔎 AI Research Assistant

AI Research Assistant is a multi-agent research platform that combines live web research, local document analysis, Retrieval-Augmented Generation (RAG), persistent memory, and local AI models in a single workflow.

The system can research a user query using both web sources and uploaded documents, analyze the collected information, generate a structured report, verify the result, automatically revise it when necessary, and export the final report as PDF or DOCX.

---

## ✨ Features

- 🤖 Multi-Agent Research Workflow
- 🌐 Live Web Research
- 📄 PDF, DOCX and TXT Document Support
- 🧠 Retrieval-Augmented Generation (RAG)
- 🔍 FAISS Vector Search
- 🧩 Local Text Embeddings
- 💾 Persistent SQLite Memory
- 💬 Follow-up Questions
- 🗂️ Research Sessions
- 📊 Live Agent Status Tracking
- ✅ Automatic Verification and Revision
- 🚀 FastAPI Backend
- 🖥️ Streamlit Web Interface
- 📄 PDF Report Export
- 📝 DOCX Report Export
- 🧪 Automated Tests with Pytest
- 🐳 Docker & Docker Compose Support
- 🔐 Environment-based Configuration

---

## 🧠 Multi-Agent Architecture

The research process is handled by four specialized agents:

### 1. Researcher

Collects information from live web sources and, when available, uploaded documents.

### 2. Analyst

Analyzes the collected material and identifies the most relevant information for the research question.

### 3. Writer

Creates the final structured research report based on the analyzed evidence.

### 4. Verifier

Checks the generated report for consistency and source support.

If a correction is required, the report is automatically sent back to the Writer for revision.

```text
User Query
    │
    ▼
Researcher
    │
    ▼
Analyst
    │
    ▼
Writer
    │
    ▼
Verifier
    │
    ├── Approved ──► Final Report
    │
    └── Revision Required
              │
              ▼
            Writer
              │
              ▼
           Verifier
```

---

## 🔎 RAG Pipeline

Uploaded documents are processed through a local RAG pipeline.

```text
Document
   │
   ▼
Text Extraction
   │
   ▼
Chunking
   │
   ▼
Local Embeddings
   │
   ▼
FAISS Vector Index
   │
   ▼
Semantic Retrieval
   │
   ▼
Relevant Context
   │
   ▼
Local LLM
```

This allows the assistant to answer questions using relevant sections of uploaded documents instead of sending the entire document to the model.

---

## 📄 Supported Documents

The platform currently supports:

- `.pdf`
- `.docx`
- `.txt`

Uploaded documents can be used together with live web research.

---

## 🧠 Persistent Memory

Research history and conversations are stored using SQLite.

The memory system supports:

- Session-based conversations
- Previous user messages
- Assistant responses
- Previous research topics
- Research results
- Follow-up questions

Using the same session name allows previous context to be reused.

---

## 📊 Live Agent Status

The Streamlit interface displays the current state of every agent in real time.

Example:

```text
✅ Researcher — Completed
✅ Analyst — Completed
⏳ Writer — Running
○ Verifier — Waiting
```

The interface also reflects automatic Writer → Verifier revision cycles.

---

## 📑 Research Reports

Completed research can be exported as:

- Markdown
- Microsoft Word (`.docx`)
- PDF (`.pdf`)

Generated reports are stored locally inside the output directory.

---

## 🏗️ Project Structure

```text
ai-research-assistant/
│
├── agents/
│   ├── analyst.py
│   ├── researcher.py
│   ├── verifier.py
│   └── writer.py
│
├── tests/
│   ├── test_agent_status.py
│   ├── test_chunking.py
│   ├── test_document_reader.py
│   ├── test_faiss.py
│   ├── test_memory.py
│   ├── test_report_exporter.py
│   ├── test_routing.py
│   └── test_web_search.py
│
├── utils/
│   ├── agent_status.py
│   ├── conversation_memory.py
│   ├── document_rag.py
│   ├── document_reader.py
│   ├── embedding.py
│   ├── page_reader.py
│   ├── report_exporter.py
│   ├── report_saver.py
│   ├── system_check.py
│   ├── text_chunker.py
│   ├── vector_store.py
│   └── web_search.py
│
├── api.py
├── config.py
├── main.py
├── settings.py
├── state.py
├── web_app.py
│
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 🛠️ Technology Stack

### Backend

- Python
- FastAPI
- Uvicorn

### Frontend

- Streamlit

### AI & Retrieval

- Local LLM through Ollama
- LangChain
- Sentence Transformers
- FAISS
- RAG

### Data & Memory

- SQLite

### Document Processing

- PDF parsing
- python-docx
- TXT parsing

### Reporting

- ReportLab
- python-docx

### Testing

- Pytest

### Deployment

- Docker
- Docker Compose

---

## ⚙️ Local Installation

### 1. Clone the repository

```bash
git clone <repository-url>
cd ai-research-assistant
```

### 2. Create a virtual environment

Windows:

```powershell
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root.

Sensitive information such as API keys should be stored only in this file.

The `.env` file is excluded from Git.

### 5. Start Ollama

Make sure Ollama is installed and the configured local model is available.

The local Ollama address defaults to:

```text
http://127.0.0.1:11434
```

The model and related settings can be configured in `settings.py`.

---

## ▶️ Running Locally

Two services are required.

### Terminal 1 — FastAPI

```powershell
uvicorn api:api --reload
```

API documentation:

```text
http://127.0.0.1:8000/docs
```

### Terminal 2 — Streamlit

```powershell
streamlit run web_app.py
```

Web interface:

```text
http://localhost:8501
```

---

## 🚀 API Endpoints

The FastAPI backend provides endpoints for:

```text
GET   /
GET   /health
POST  /upload
POST  /research
POST  /research/start
GET   /research/status/{job_id}
POST  /ask
GET   /sessions
GET   /reports
```

Interactive Swagger documentation is available at:

```text
http://127.0.0.1:8000/docs
```

---

## 🧪 Automated Tests

The project includes automated tests for core components such as:

- Document reading
- Text chunking
- FAISS retrieval
- Persistent memory
- Agent status tracking
- Report exporting
- Agent routing
- Web search utilities

Run all tests with:

```powershell
python -m pytest tests -q
```

---

## 🐳 Docker

The project includes both a `Dockerfile` and `docker-compose.yml`.

Docker Compose starts two services:

```text
ai-research-api
ai-research-web
```

### Build

```powershell
docker compose build
```

### Start

```powershell
docker compose up -d
```

### Check containers

```powershell
docker compose ps
```

### Open the services

FastAPI:

```text
http://127.0.0.1:8000/docs
```

Streamlit:

```text
http://localhost:8501
```

### Stop

```powershell
docker compose down
```

Inside Docker, the API communicates with the host Ollama service through:

```text
http://host.docker.internal:11434
```

---

## 🔐 Security

Sensitive and generated files are excluded from version control, including:

```text
.env
.venv/
outputs/
documents/
documents/uploads/
*.db
*.sqlite
*.sqlite3
__pycache__/
.pytest_cache/
```

Never commit API keys or credentials directly to the repository.

---

## 🔄 Research Workflow

```text
User enters a research question
          │
          ▼
Optional document upload
          │
          ▼
Web + Document Retrieval
          │
          ▼
Researcher
          │
          ▼
Analyst
          │
          ▼
Writer
          │
          ▼
Verifier
          │
          ├── Revision needed ──► Writer
          │
          ▼
Final Research Report
          │
          ├── PDF
          └── DOCX
```

---

## 🎯 Project Goals

This project was developed to explore how a production-style research assistant can combine:

- Multi-agent AI systems
- Retrieval-Augmented Generation
- Semantic search
- Local AI models
- Live web research
- Persistent memory
- API-based architecture
- Automated verification
- Containerized deployment

The architecture is designed to be modular so that individual components such as the embedding model, LLM, retrieval system, agents, and user interface can be extended independently.

---

## 📌 Future Improvements

Possible future extensions include:

- Streaming model responses
- Source credibility scoring
- Additional document formats
- User authentication
- Research history search
- Advanced citation verification
- Cloud deployment
- Additional local and remote LLM providers
- Improved observability and logging

---

## 👩‍💻 Developer

Developed by **Betül Altunyuva**

Software Engineering