from state import ResearchState
from config import llm


def writer_agent(state: ResearchState):
    query = state["query"]
    analysis = state["analysis"]
    sources = state.get("sources", [])
    verification_report = state.get("verification_report", "")
    revision_count = state.get("revision_count", 0)

    if verification_report:
        print("[Writer Agent] Rapor doğrulama sonucuna göre düzeltiliyor...")
    else:
        print("[Writer Agent] Nihai rapor hazırlanıyor...")

    source_list = ""

    for index, source in enumerate(sources, start=1):
        source_list += f"""
[{index}] {source["title"]}
{source["url"]}
"""

    revision_instruction = ""

    if verification_report:
        revision_instruction = f"""
Önceki rapor doğrulama uzmanı tarafından kontrol edildi.

DOĞRULAMA RAPORU:

{verification_report}

Bu sorunları dikkate alarak raporu düzelt.
Hatalı, desteklenmeyen veya yarım kalmış ifadeleri çıkar ya da düzelt.
"""

    prompt = f"""
Sen kaynaklara bağlı çalışan profesyonel bir araştırma raporu yazarısın.

Araştırma konusu:

{query}

Analiz:

{analysis}

Mevcut kaynaklar:

{source_list}

{revision_instruction}

Kurallar:

- Yalnızca verilen analiz ve kaynakları kullan.
- Kaynaklarda bulunmayan bilgi uydurma.
- Sayı, tarih veya istatistik icat etme.
- Kaynak destekli ifadelerde [1], [2], [3] gibi numaralar kullan.
- Kaynak sayısını olduğundan fazla gösterme.
- Eksik veya yarım cümle bırakma.
- Emin olmadığın bilgileri kesin gerçek gibi sunma.

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

    for index, source in enumerate(sources, start=1):
        references += (
            f"\n[{index}] {source['title']}\n"
            f"{source['url']}\n"
        )

    new_revision_count = revision_count

    if verification_report:
        new_revision_count += 1

    return {
        "final_answer": response.content + references,
        "revision_count": new_revision_count
    }