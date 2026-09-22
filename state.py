from typing import TypedDict


class ResearchState(TypedDict, total=False):
    query: str
    conversation_history: str
    previous_research: str
    session_id: str
    job_id: str

    # Web kaynakları
    sources: list[dict[str, str]]

    # Yüklenen belge
    document_path: str
    document_context: str

    # Agent çıktıları
    research: str
    analysis: str
    final_answer: str
    verification_report: str

    revision_count: int