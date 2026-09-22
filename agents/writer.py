from state import ResearchState
from config import llm
from utils.agent_status import update_agent_status


def writer_agent(state: ResearchState):
    job_id = state.get(
        "job_id",
        ""
    )

    update_agent_status(
        job_id,
        "analyst",
        "completed"
    )

    if state.get("verification_report"):
        update_agent_status(
            job_id,
            "verifier",
            "waiting"
        )

    update_agent_status(
        job_id,
        "writer",
        "running"
    )

    query = state["query"]
    analysis = state["analysis"]

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

    verification_report = state.get(
        "verification_report",
        ""
    )

    revision_count = state.get(
        "revision_count",
        0
    )

    if verification_report:
        print(
            "[Writer Agent] "
            "Rapor doğrulama sonucuna göre "
            "düzeltiliyor..."
        )
    else:
        print(
            "[Writer Agent] "
            "Nihai rapor hazırlanıyor..."
        )

    web_source_list = ""

    for index, source in enumerate(
        sources,
        start=1
    ):
        web_source_list += f"""
[WEB-{index}] {source.get("title", "")}
{source.get("url", "")}
"""

    if not web_source_list:
        web_source_list = (
            "Web kaynağı kullanılmadı."
        )

    if not document_context:
        document_context = (
            "Belge kaynağı kullanılmadı."
        )

    revision_instruction = ""

    if verification_report:
        revision_instruction = f"""
Önceki rapor doğrulama uzmanı tarafından
kontrol edildi.

DOĞRULAMA RAPORU:

{verification_report}

Bu sorunları dikkate alarak raporu düzelt.

Hatalı, desteklenmeyen veya yarım kalmış
ifadeleri çıkar ya da düzelt.
"""

    prompt = f"""
Sen kaynaklara bağlı çalışan profesyonel
bir araştırma raporu yazarısın.

ARAŞTIRMA KONUSU:

{query}


ANALİZ:

{analysis}


WEB KAYNAKLARI:

{web_source_list}


BELGE KAYNAĞI:

Dosya:
{document_path if document_path else "Yok"}

İlgili belge bölümleri:

{document_context}


{revision_instruction}


Kurallar:

- Yalnızca verilen analiz ve kaynakları kullan.
- Kendi genel bilgini ekleme.
- Kaynaklarda bulunmayan bilgi uydurma.
- Sayı, tarih veya istatistik icat etme.
- Web kaynağı kullandığında [WEB-1], [WEB-2], [WEB-3]
  biçimindeki atıfları kullan.
- Belge bilgisi kullandığında [DOC-1],
  [DOC-2] biçimindeki atıfları kullan.
- Web ve belge kaynaklarını birbirine
  karıştırma.
- Kaynak sayısını olduğundan fazla gösterme.
- Eksik veya yarım cümle bırakma.
- Emin olmadığın bilgileri kesin gerçek
  gibi sunma.

Rapor şu bölümleri içersin:

# Başlık

## Kısa Giriş

## Temel Bulgular

## Değerlendirme

## Sonuç

Cevabı Türkçe yaz.
"""

    response = llm.invoke(prompt)

    references = "\n\n## Kaynaklar\n"

    if sources:
        references += "\n### Web Kaynakları\n"

        for index, source in enumerate(
            sources,
            start=1
        ):
            references += (
                f"\n[WEB-{index}] "
                f"{source.get('title', '')}\n"
                f"{source.get('url', '')}\n"
            )

    if document_path:
        references += (
            "\n### Belge Kaynağı\n"
            f"\n{document_path}\n"
        )

    new_revision_count = revision_count

    if verification_report:
        new_revision_count += 1

        update_agent_status(
        job_id,
        "writer",
        "completed"
    )

    return {
        "final_answer":
            response.content + references,
        "revision_count":
            new_revision_count
    }