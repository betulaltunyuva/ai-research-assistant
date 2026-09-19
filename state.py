from typing import TypedDict


class ResearchState(TypedDict, total=False):
    query: str
    sources: list[dict[str, str]]
    research: str
    analysis: str
    final_answer: str
    verification_report: str
    revision_count: int