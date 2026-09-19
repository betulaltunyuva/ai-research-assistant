from state import ResearchState
from config import llm


def analyst_agent(state: ResearchState):
    research = state["research"]
    sources = state.get("sources", [])

    print("[Analyst Agent] Bilgiler analiz ediliyor...")

    source_list = ""

    for index, source in enumerate(sources, start=1):
        source_list += f"""
[{index}]
Başlık: {source["title"]}
URL: {source["url"]}
"""

    prompt = f"""
Sen dikkatli bir araştırma analistisin.

Araştırma notları:
{research}

Kullanılan kaynaklar:
{source_list}

Görevin:
- Yalnızca verilen araştırma notları ve kaynaklara dayan.
- Kaynaklarda bulunmayan sayı, tarih, istatistik veya iddia üretme.
- Bilgileri karşılaştır ve en önemli bulguları çıkar.
- Kaynak numaralarını [1], [2] şeklinde koru.
- Bir bilginin kaynağı belli değilse kesin bir gerçek gibi yazma.
- Nihai raporu hazırlayacak yazara temiz bir analiz hazırla.

Cevabı Türkçe yaz.
"""

    response = llm.invoke(prompt)

    return {
        "analysis": response.content
    }