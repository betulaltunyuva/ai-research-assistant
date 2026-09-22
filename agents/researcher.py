from state import ResearchState
from config import llm
from utils.agent_status import update_agent_status

from utils.web_search import search_web
from utils.page_reader import read_web_page
from utils.document_rag import (
    prepare_document,
    retrieve_context
)

from settings import (
    SEARCH_RESULT_COUNT,
    PAGE_MAX_CHARS
)


def researcher_agent(state: ResearchState):
    job_id = state.get(
        "job_id",
        ""
    )

    update_agent_status(
        job_id,
        "researcher",
        "running"
    )
    query = state["query"]

    conversation_history = state.get(
        "conversation_history",
        ""
    )

    previous_research = state.get(
        "previous_research",
        ""
    )

    document_path = state.get(
        "document_path",
        ""
    ).strip()

    print(
        "\n[Researcher Agent] "
        "Araştırma başlatılıyor..."
    )

    # -------------------------------------------------
    # 1. WEB ARAŞTIRMASI
    # -------------------------------------------------

    print(
        "[Researcher Agent] "
        "Web araştırması yapılıyor..."
    )

    sources = search_web(
        query,
        max_results=SEARCH_RESULT_COUNT
    )

    source_text = ""

    for index, source in enumerate(
        sources,
        start=1
    ):
        print(
            f"[Researcher Agent] "
            f"WEB KAYNAĞI [WEB-{index}]/{len(sources)} okunuyor: "
            f"{source.get('domain', 'bilinmeyen kaynak')}"
        )

        page_content = read_web_page(
            source["url"],
            max_chars=PAGE_MAX_CHARS
        )

        if not page_content:
            page_content = source.get(
                "snippet",
                ""
            )

        source["content"] = page_content

        source_text += f"""
WEB KAYNAĞI [{index}]

Başlık:
{source.get("title", "")}

Alan adı:
{source.get("domain", "")}

URL:
{source.get("url", "")}

İçerik:
{page_content}

------------------------------
"""

    # -------------------------------------------------
    # 2. BELGE / RAG ARAŞTIRMASI
    # -------------------------------------------------

    document_context = ""

    if document_path:
        print(
            "[Researcher Agent] "
            "Yüklenen belgede araştırma yapılıyor..."
        )

        prepared_document = prepare_document(
            document_path
        )

        retrieved = retrieve_context(
            prepared_document,
            query,
            top_k=3
        )

        document_context = retrieved[
            "context"
        ]

        print(
            "[Researcher Agent] "
            f"{len(retrieved['results'])} "
            "ilgili belge parçası bulundu."
        )

    # -------------------------------------------------
    # 3. KAYNAK KONTROLÜ
    # -------------------------------------------------

    if not sources and not document_context:
        update_agent_status(
            job_id,
            "researcher",
            "completed"
        )
        return {
            "research":
                "Araştırma için kullanılabilir "
                "web veya belge kaynağı bulunamadı.",
            "sources": [],
            "document_context": ""
        }

    if not source_text:
        source_text = (
            "Web kaynağı bulunamadı."
        )

    if not document_context:
        document_context = (
            "Yüklenmiş belge kaynağı yok."
        )

    # -------------------------------------------------
    # 4. RESEARCHER LLM
    # -------------------------------------------------

    prompt = f"""
Sen dikkatli bir araştırma uzmanısın.

ARAŞTIRMA KONUSU:

{query}

ÖNCEKİ KONUŞMA GEÇMİŞİ:

{conversation_history if conversation_history else "Önceki konuşma yok."}


ÖNCEKİ ARAŞTIRMA:

{previous_research if previous_research else "Önceki araştırma yok."}

WEB KAYNAKLARI:

{source_text}


YÜKLENEN BELGEDEN BULUNAN İLGİLİ BÖLÜMLER:

{document_context}


Görevin:

- Yalnızca yukarıda verilen kaynakları kullan.
- Web ve belge kaynaklarını birlikte değerlendir.
- Web kaynaklarında bulunmayan bilgi üretme.
- Belge içeriğinde bulunmayan bilgi üretme.
- Sayı, tarih veya istatistik uydurma.
- Web kaynağı kullanırken [WEB-1], [WEB-2], [WEB-3]
  biçimindeki kaynak numarasını koru.
- Belge kaynağı kullanırken [DOC-1],
  [DOC-2] gibi kaynak numarasını koru.
- Kaynaklar arasında çelişki varsa bunu belirt.
- Nihai raporu hazırlayacak analiste
  düzenli araştırma notları oluştur.
- Kullanıcı önceki konuşmaya atıf yapıyorsa konuşma geçmişini dikkate al.
- Önceki araştırmadaki bilgileri yalnızca yeni soruyla ilgiliyse kullan.

Cevabı Türkçe yaz.
"""

    response = llm.invoke(
        prompt
    )

    return {
        "research": response.content,
        "sources": sources,
        "document_context":
            document_context
    }