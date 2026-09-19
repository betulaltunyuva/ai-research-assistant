from urllib.parse import urlparse

from ddgs import DDGS


HIGH_QUALITY_DOMAINS = (
    "arxiv.org",
    "ieee.org",
    "acm.org",
    "springer.com",
    "nature.com",
    "sciencedirect.com",
    ".edu",
    ".gov",
)

OFFICIAL_TECH_DOMAINS = (
    "microsoft.com",
    "github.com",
    "github.blog",
    "google.com",
    "developers.google.com",
    "openai.com",
    "anthropic.com",
)

LOW_PRIORITY_DOMAINS = (
    "medium.com",
    "wordpress.com",
    "blogspot.com",
)


def get_domain(url: str) -> str:
    try:
        return (
            urlparse(url)
            .netloc
            .lower()
            .replace("www.", "")
        )
    except Exception:
        return ""


def calculate_source_score(url: str) -> int:
    domain = get_domain(url)

    score = 0

    if url.startswith("https://"):
        score += 1

    if any(
        trusted in domain
        for trusted in HIGH_QUALITY_DOMAINS
    ):
        score += 6

    elif any(
        trusted in domain
        for trusted in OFFICIAL_TECH_DOMAINS
    ):
        score += 4

    if any(
        low_quality in domain
        for low_quality in LOW_PRIORITY_DOMAINS
    ):
        score -= 2

    return score


def search_web(query: str, max_results: int = 3):
    try:
        # Daha fazla sonuç toplayıp içlerinden
        # daha güvenilir olanları seçiyoruz.
        search_count = max(
            max_results * 5,
            15
        )

        raw_results = DDGS().text(
            query,
            max_results=search_count
        )

        sources = []
        seen_urls = set()

        for result in raw_results:
            url = result.get("href", "")

            if not url:
                continue

            if not url.startswith(
                ("http://", "https://")
            ):
                continue

            if url in seen_urls:
                continue

            seen_urls.add(url)

            sources.append({
                "title": result.get(
                    "title",
                    ""
                ).strip(),

                "url": url,

                "snippet": result.get(
                    "body",
                    ""
                ).strip(),

                "domain": get_domain(url),

                "quality_score":
                    calculate_source_score(url)
            })

        sources.sort(
            key=lambda source:
                source["quality_score"],
            reverse=True
        )

        return sources[:max_results]

    except Exception as e:
        print(
            f"[Web Search] Arama hatası: {e}"
        )
        return []