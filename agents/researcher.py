from state import ResearchState
from config import llm
from utils.web_search import search_web
from utils.page_reader import read_web_page
from settings import SEARCH_RESULT_COUNT, PAGE_MAX_CHARS


def researcher_agent(state: ResearchState):
    query = state["query"]

    print("\n[Researcher Agent] Web araştırması yapılıyor...")

    sources = search_web(
        query,
        max_results=SEARCH_RESULT_COUNT
    )

    if not sources:
        return {
            "research": "Web araştırmasında kaynak bulunamadı.",
            "sources": []
        }

    source_text = ""

    for index, source in enumerate(sources, start=1):
        print(
            f"[Researcher Agent] Kaynak {index}/{len(sources)} okunuyor: "
            f"{source.get('domain', 'bilinmeyen kaynak')}"
        )

        page_content = read_web_page(
            source["url"],
            max_chars=PAGE_MAX_CHARS
        )
        if not page_content:
            page_content = source["snippet"]

        source["content"] = page_content

        source_text += f"""
KAYNAK [{index}]

Başlık:
{source["title"]}

Alan adı:
{source.get("domain", "")}

URL:
{source["url"]}

İçerik:
{page_content}

------------------------------
"""

    prompt = f"""
Sen dikkatli bir araştırma uzmanısın.

Araştırma konusu:

{query}

Aşağıda internetten bulunan gerçek web sayfalarının
içerikleri bulunmaktadır.

{source_text}

Görevin:

- Yalnızca verilen kaynak içeriklerini kullan.
- En önemli bilgileri çıkar.
- Kaynaklar arasındaki benzerlikleri ve farklılıkları belirle.
- Desteklenmeyen bilgi üretme.
- Sayı veya istatistik uydurma.
- Her önemli iddianın yanında [1], [2] veya [3]
  şeklinde ilgili kaynak numarasını belirt.
- Nihai raporu hazırlayacak analiste düzenli
  araştırma notları oluştur.

Cevabı Türkçe yaz.
"""

    response = llm.invoke(prompt)

    return {
        "research": response.content,
        "sources": sources
    }