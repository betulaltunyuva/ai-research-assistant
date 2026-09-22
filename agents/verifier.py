from state import ResearchState
from config import llm
from utils.agent_status import update_agent_status


def verifier_agent(state: ResearchState):
    job_id = state.get(
        "job_id",
        ""
    )

    update_agent_status(
        job_id,
        "writer",
        "completed"
    )

    update_agent_status(
        job_id,
        "verifier",
        "running"
    )

    final_answer = state["final_answer"]

    sources = state.get(
        "sources",
        []
    )

    document_context = state.get(
        "document_context",
        ""
    )

    document_path = state.get(
        "document_path",
        ""
    )

    print(
        "[Verifier Agent] "
        "Web ve belge kaynakları doğrulanıyor..."
    )

    web_source_text = ""

    for index, source in enumerate(
        sources,
        start=1
    ):
        web_source_text += f"""
WEB KAYNAĞI [WEB-{index}]

Başlık:
{source.get("title", "")}

URL:
{source.get("url", "")}

İçerik:
{source.get(
    "content",
    source.get("snippet", "")
)}

------------------------------
"""

    if not web_source_text:
        web_source_text = (
            "Web kaynağı kullanılmadı."
        )

    if not document_context:
        document_context = (
            "Belge kaynağı kullanılmadı."
        )

    prompt = f"""
Sen titiz bir kaynak doğrulama uzmanısın.

Aşağıdaki araştırma raporunu verilen
web ve belge kaynaklarıyla karşılaştır.


RAPOR:

{final_answer}


WEB KAYNAKLARI:

{web_source_text}


BELGE KAYNAĞI:

Dosya:
{document_path if document_path else "Yok"}

İlgili belge bölümleri:

{document_context}


Kontrol et:

- Rapordaki önemli iddialar gerçekten
  verilen kaynaklarda var mı?
- Sayılar, tarihler ve istatistikler
  destekleniyor mu?
- [WEB-1], [WEB-2], [WEB-3] atıfları
  doğru web kaynaklarına mı ait?
- [DOC-1], [DOC-2] gibi atıflar
  gerçekten ilgili belge parçalarına mı ait?
- Kaynaklarda bulunmayan bilgiler
  eklenmiş mi?
- Web ve belge kaynakları birbirine
  yanlış şekilde karıştırılmış mı?
- Kaynaklar arasında çelişen ifadeler
  var mı?
- Eksik veya yarım kalmış cümle var mı?

Kısa ve net bir doğrulama raporu hazırla.

Şu formatı kullan:

DURUM: UYGUN

veya

DURUM: DÜZELTME GEREKLİ


SORUNLAR:

- Sorun varsa maddeler halinde yaz.
- Sorun yoksa
  "Belirgin bir sorun tespit edilmedi."
  yaz.

Cevabı Türkçe yaz.
"""

    response = llm.invoke(prompt)

    update_agent_status(
        job_id,
        "verifier",
        "completed"
    )

    return {
        "verification_report":
            response.content
    }