import json
import os
import re
from datetime import datetime


def create_safe_filename(text: str) -> str:
    text = text.lower().strip()

    text = text.replace("ç", "c")
    text = text.replace("ğ", "g")
    text = text.replace("ı", "i")
    text = text.replace("ö", "o")
    text = text.replace("ş", "s")
    text = text.replace("ü", "u")

    text = re.sub(r"[^a-z0-9]+", "-", text)

    return text.strip("-")[:60]


def save_history(
    query: str,
    status: str,
    report_path: str = "",
    revision_count: int = 0,
    duration_seconds: float = 0,
    source_count: int = 0,
    error: str = ""
):
    os.makedirs("outputs", exist_ok=True)

    history_path = os.path.join(
        "outputs",
        "history.jsonl"
    )

    history_item = {
        "query": query,
        "status": status,
        "report_path": report_path,
        "revision_count": revision_count,
        "duration_seconds": round(duration_seconds, 2),
        "source_count": source_count,
        "error": error,
        "created_at": datetime.now().isoformat()
    }

    with open(
        history_path,
        "a",
        encoding="utf-8"
    ) as file:
        file.write(
            json.dumps(
                history_item,
                ensure_ascii=False
            ) + "\n"
        )


def save_report(
    query: str,
    result: dict,
    duration_seconds: float
):
    os.makedirs(
        "outputs/reports",
        exist_ok=True
    )

    timestamp = datetime.now().strftime(
        "%Y-%m-%d_%H-%M-%S"
    )

    safe_query = create_safe_filename(query)

    filename = (
        f"{timestamp}_{safe_query}.md"
    )

    report_path = os.path.join(
        "outputs",
        "reports",
        filename
    )

    final_answer = result.get(
        "final_answer",
        ""
    )

    verification = result.get(
        "verification_report",
        ""
    )

    revision_count = result.get(
        "revision_count",
        0
    )

    source_count = len(
        result.get("sources", [])
    )

    markdown_content = f"""# AI Research Assistant Report

## Araştırma Konusu

{query}

---

{final_answer}

---

## Doğrulama Raporu

{verification}

---

## Sistem Bilgisi

- Kullanılan kaynak sayısı: {source_count}
- Otomatik düzeltme sayısı: {revision_count}
- Toplam süre: {duration_seconds:.2f} saniye
- Oluşturulma zamanı: {datetime.now().strftime("%d.%m.%Y %H:%M:%S")}
"""

    with open(
        report_path,
        "w",
        encoding="utf-8"
    ) as file:
        file.write(markdown_content)

    save_history(
        query=query,
        status="success",
        report_path=report_path,
        revision_count=revision_count,
        duration_seconds=duration_seconds,
        source_count=source_count
    )

    return report_path