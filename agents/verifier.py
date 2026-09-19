from state import ResearchState
from config import llm


def verifier_agent(state: ResearchState):
    final_answer = state["final_answer"]
    sources = state.get("sources", [])

    print("[Verifier Agent] Kaynaklar ve rapor doğrulanıyor...")

    source_text = ""

    for index, source in enumerate(sources, start=1):
        source_text += f"""
KAYNAK [{index}]

Başlık:
{source["title"]}

URL:
{source["url"]}

İçerik:
{source.get("content", source.get("snippet", ""))}

------------------------------
"""

    prompt = f"""
Sen titiz bir kaynak doğrulama uzmanısın.

Aşağıdaki araştırma raporunu verilen kaynaklarla karşılaştır.

RAPOR:

{final_answer}

KAYNAKLAR:

{source_text}

Kontrol et:

- Rapordaki önemli iddialar gerçekten kaynaklarda var mı?
- Sayılar, tarihler ve istatistikler destekleniyor mu?
- [1], [2], [3] atıfları doğru kaynakları mı gösteriyor?
- Kaynaklarda bulunmayan bilgiler eklenmiş mi?
- Birbiriyle çelişen ifadeler var mı?
- Eksik veya yarım kalmış cümle var mı?

Kısa ve net bir doğrulama raporu hazırla.

Şu formatı kullan:

DURUM: UYGUN
veya
DURUM: DÜZELTME GEREKLİ

SORUNLAR:
- Sorun varsa maddeler halinde yaz.
- Sorun yoksa "Belirgin bir sorun tespit edilmedi." yaz.

Cevabı Türkçe yaz.
"""

    response = llm.invoke(prompt)

    return {
        "verification_report": response.content
    }