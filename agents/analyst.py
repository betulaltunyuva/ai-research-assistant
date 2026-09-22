from state import ResearchState
from config import llm
from utils.agent_status import update_agent_status

def analyst_agent(state: ResearchState):
    job_id = state.get(
        "job_id",
        ""
    )

    update_agent_status(
        job_id,
        "researcher",
        "completed"
    )

    update_agent_status(
        job_id,
        "analyst",
        "running"
    )

    research = state["research"]
    sources = state.get("sources", [])
    document_context = state.get(
        "document_context",
        ""
    )
    document_path = state.get(
        "document_path",
        ""
    )

    print(
        "[Analyst Agent] "
        "Web ve belge bilgileri analiz ediliyor..."
    )

    web_source_list = ""

    for index, source in enumerate(
        sources,
        start=1
    ):
        web_source_list += f"""
[WEB-{index}]
Başlık:{source.get("title", "")}
URL: {source.get("url", "")}
"""

    if not web_source_list:
        web_source_list = (
            "Web kaynağı bulunmuyor."
        )

    if not document_context:
        document_context = (
            "Belge kaynağı bulunmuyor."
        )

    prompt = f"""
Sen dikkatli bir araştırma analistisin.

ARAŞTIRMA NOTLARI:

{research}


WEB KAYNAKLARI:

{web_source_list}


BELGE KAYNAĞI:

Dosya:
{document_path if document_path else "Yok"}

İlgili belge bölümleri:

{document_context}


Görevin:

- Yalnızca verilen araştırma notları ve kaynaklara dayan.
- Web ve belge bilgilerini birlikte analiz et.
- Kaynaklarda bulunmayan bilgi üretme.
- Sayı, tarih veya istatistik uydurma.
- Web kaynaklarının [WEB-1], [WEB-2], [WEB-3]
  biçimindeki numaralarını koru.
- Belge kaynaklarının [DOC-1],
  [DOC-2] biçimindeki numaralarını koru.
- Web ve belge arasında çelişki varsa belirt.
- En önemli bulguları çıkar.
- Nihai raporu hazırlayacak yazara
  temiz ve düzenli bir analiz hazırla.

Cevabı Türkçe yaz.
"""

    response = llm.invoke(prompt)

    update_agent_status(
        job_id,
        "analyst",
        "completed"
    )

    return {
        "analysis": response.content
    }