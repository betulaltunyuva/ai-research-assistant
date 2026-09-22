from pathlib import Path
from uuid import uuid4

import shutil
import time

from fastapi import (
    FastAPI,
    UploadFile,
    File,
    HTTPException,
    BackgroundTasks
)

from pydantic import BaseModel

from main import app as research_app
from config import llm

from utils.conversation_memory import (
    init_memory,
    save_message,
    get_recent_messages,
    save_research,
    get_last_research,
    get_sessions
)

from utils.report_saver import save_report
from utils.system_check import check_ollama

from utils.agent_status import (
    create_job_status,
    update_job_status,
    save_job_result,
    save_job_error,
    get_job_status
)

from settings import MODEL_NAME


api = FastAPI(
    title="AI Research Assistant API",
    version="2.0"
)


UPLOAD_DIR = Path(
    "documents/uploads"
)

UPLOAD_DIR.mkdir(
    parents=True,
    exist_ok=True
)


ALLOWED_EXTENSIONS = {
    ".pdf",
    ".docx",
    ".txt"
}


init_memory()


class ResearchRequest(BaseModel):
    query: str
    session_id: str = "default"
    document_path: str = ""


class AskRequest(BaseModel):
    question: str
    session_id: str = "default"


# ---------------------------------------------------------
# YARDIMCI FONKSİYONLAR
# ---------------------------------------------------------

def validate_research_request(
    request: ResearchRequest
):
    query = request.query.strip()

    if not query:
        raise HTTPException(
            status_code=400,
            detail="Araştırma konusu boş bırakılamaz."
        )

    session_id = (
        request.session_id.strip()
        or "default"
    )

    document_path = (
        request.document_path.strip()
    )

    if document_path:
        if not Path(document_path).exists():
            raise HTTPException(
                status_code=404,
                detail="Belge bulunamadı."
            )

    return (
        query,
        session_id,
        document_path
    )


def execute_research(
    query: str,
    session_id: str,
    document_path: str,
    job_id: str = ""
):
    ollama_ready, message = check_ollama(
        MODEL_NAME
    )

    if not ollama_ready:
        raise RuntimeError(message)

    recent_messages = get_recent_messages(
        session_id=session_id,
        limit=6
    )

    last_research = get_last_research(
        session_id=session_id
    )

    conversation_history = ""

    for message_item in recent_messages:
        conversation_history += (
            f"{message_item['role']}: "
            f"{message_item['content']}\n"
        )

    previous_research = ""

    if last_research:
        previous_research = (
            f"Önceki araştırma konusu:\n"
            f"{last_research['query']}\n\n"
            f"Önceki cevap:\n"
            f"{last_research['final_answer']}"
        )

    start_time = time.perf_counter()

    result = research_app.invoke({
        "query": query,
        "session_id": session_id,
        "job_id": job_id,
        "document_path": document_path,
        "conversation_history":
            conversation_history,
        "previous_research":
            previous_research,
        "revision_count": 0
    })

    duration_seconds = (
        time.perf_counter() - start_time
    )

    report_path = save_report(
        query,
        result,
        duration_seconds
    )

    save_message(
        "user",
        query,
        session_id=session_id
    )

    save_message(
        "assistant",
        result.get(
            "final_answer",
            ""
        ),
        session_id=session_id
    )

    save_research(
        query=query,
        final_answer=result.get(
            "final_answer",
            ""
        ),
        sources=result.get(
            "sources",
            []
        ),
        document_path=document_path,
        session_id=session_id
    )

    return {
        "session_id": session_id,
        "query": query,
        "final_answer": result.get(
            "final_answer",
            ""
        ),
        "verification_report":
            result.get(
                "verification_report",
                ""
            ),
        "revision_count":
            result.get(
                "revision_count",
                0
            ),
        "source_count": len(
            result.get(
                "sources",
                []
            )
        ),
        "duration_seconds": round(
            duration_seconds,
            2
        ),
        "report_path": report_path
    }


def run_research_job(
    job_id: str,
    query: str,
    session_id: str,
    document_path: str
):
    try:
        update_job_status(
            job_id,
            "running"
        )

        result = execute_research(
            query=query,
            session_id=session_id,
            document_path=document_path,
            job_id=job_id
        )

        save_job_result(
            job_id,
            result
        )

    except Exception as error:
        save_job_error(
            job_id,
            str(error)
        )


# ---------------------------------------------------------
# TEMEL ENDPOINTLER
# ---------------------------------------------------------

@api.get("/")
def root():
    return {
        "project": "AI Research Assistant",
        "version": "2.0",
        "status": "running"
    }


@api.get("/health")
def health():
    return {
        "status": "ok"
    }


# ---------------------------------------------------------
# DOSYA YÜKLEME
# ---------------------------------------------------------

@api.post("/upload")
def upload_document(
    file: UploadFile = File(...)
):
    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="Dosya adı bulunamadı."
        )

    safe_filename = Path(
        file.filename
    ).name

    extension = Path(
        safe_filename
    ).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=(
                "Sadece PDF, DOCX ve TXT "
                "dosyaları destekleniyor."
            )
        )

    file_path = (
        UPLOAD_DIR /
        safe_filename
    )

    with open(
        file_path,
        "wb"
    ) as buffer:
        shutil.copyfileobj(
            file.file,
            buffer
        )

    return {
        "message":
            "Dosya başarıyla yüklendi.",
        "file_name":
            safe_filename,
        "file_type":
            extension.replace(".", ""),
        "file_path":
            str(file_path)
    }


# ---------------------------------------------------------
# NORMAL / SENKRON ARAŞTIRMA
# ---------------------------------------------------------

@api.post("/research")
def research(
    request: ResearchRequest
):
    query, session_id, document_path = (
        validate_research_request(
            request
        )
    )

    try:
        return execute_research(
            query=query,
            session_id=session_id,
            document_path=document_path
        )

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=str(error)
        )


# ---------------------------------------------------------
# CANLI AGENT DURUMU İÇİN ARAŞTIRMA
# ---------------------------------------------------------

@api.post("/research/start")
def start_research_job(
    request: ResearchRequest,
    background_tasks: BackgroundTasks
):
    query, session_id, document_path = (
        validate_research_request(
            request
        )
    )

    job_id = uuid4().hex

    create_job_status(
        job_id
    )

    background_tasks.add_task(
        run_research_job,
        job_id,
        query,
        session_id,
        document_path
    )

    return {
        "job_id": job_id,
        "status": "waiting"
    }


@api.get("/research/status/{job_id}")
def research_status(
    job_id: str
):
    status = get_job_status(
        job_id
    )

    if status is None:
        raise HTTPException(
            status_code=404,
            detail="Araştırma işi bulunamadı."
        )

    return {
        "job_id": job_id,
        **status
    }


# ---------------------------------------------------------
# DEVAM SORUSU
# ---------------------------------------------------------

@api.post("/ask")
def ask_follow_up(
    request: AskRequest
):
    question = request.question.strip()

    if not question:
        raise HTTPException(
            status_code=400,
            detail="Soru boş bırakılamaz."
        )

    session_id = (
        request.session_id.strip()
        or "default"
    )

    recent_messages = get_recent_messages(
        session_id=session_id,
        limit=6
    )

    last_research = get_last_research(
        session_id=session_id
    )

    if not last_research:
        raise HTTPException(
            status_code=404,
            detail=(
                "Bu oturumda önceki "
                "araştırma bulunamadı."
            )
        )

    conversation_history = ""

    for message in recent_messages:
        conversation_history += (
            f"{message['role']}: "
            f"{message['content']}\n"
        )

    prompt = f"""
Sen AI Research Assistant'ın devam
sorularını cevaplayan asistanısın.

ÖNCEKİ ARAŞTIRMA KONUSU:

{last_research["query"]}


ÖNCEKİ ARAŞTIRMA CEVABI:

{last_research["final_answer"]}


SON KONUŞMALAR:

{conversation_history}


YENİ SORU:

{question}


Kurallar:

- Yalnızca önceki araştırma ve
  konuşmalardaki bilgilere dayan.
- Yeni bilgi uydurma.
- Önceki kaynak numaralarını mümkünse koru.
- Cevap mevcut bilgilerden çıkarılamıyorsa
  "Bu bilgi mevcut araştırmada bulunmuyor."
  şeklinde belirt.
- Cevabı açık ve kısa yaz.

Cevabı Türkçe yaz.
"""

    try:
        response = llm.invoke(
            prompt
        )

        answer = response.content

        save_message(
            "user",
            question,
            session_id=session_id
        )

        save_message(
            "assistant",
            answer,
            session_id=session_id
        )

        return {
            "session_id": session_id,
            "question": question,
            "answer": answer
        }

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=str(error)
        )


# ---------------------------------------------------------
# OTURUMLAR
# ---------------------------------------------------------

@api.get("/sessions")
def list_sessions():
    sessions = get_sessions()

    return {
        "count": len(sessions),
        "sessions": sessions
    }


# ---------------------------------------------------------
# RAPORLAR
# ---------------------------------------------------------

@api.get("/reports")
def list_reports():
    reports_directory = Path(
        "outputs/reports"
    )

    if not reports_directory.exists():
        return {
            "count": 0,
            "reports": []
        }

    report_files = sorted(
        reports_directory.glob("*.md"),
        key=lambda path:
            path.stat().st_mtime,
        reverse=True
    )

    reports = []

    for report_path in report_files:
        reports.append({
            "file_name":
                report_path.name,
            "file_path":
                str(report_path),
            "size_bytes":
                report_path.stat().st_size
        })

    return {
        "count": len(reports),
        "reports": reports
    }