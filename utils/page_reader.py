import requests
from bs4 import BeautifulSoup


def read_web_page(url: str, max_chars: int = 1000):
    try:
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 Chrome/120 Safari/537.36"
            )
        }

        response = requests.get(
            url,
            headers=headers,
            timeout=10
        )

        response.raise_for_status()

        content_type = response.headers.get(
            "Content-Type",
            ""
        ).lower()

        if "text/html" not in content_type:
            return ""

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        for tag in soup([
            "script",
            "style",
            "nav",
            "footer",
            "header",
            "aside",
            "form"
        ]):
            tag.decompose()

        useful_parts = []

        for element in soup.find_all(
            ["h1", "h2", "h3", "p", "li"]
        ):
            text = element.get_text(
                separator=" ",
                strip=True
            )

            text = " ".join(text.split())

            if len(text) >= 30:
                useful_parts.append(text)

        page_text = " ".join(useful_parts)

        return page_text[:max_chars]

    except Exception as e:
        print(
            f"[Page Reader] Sayfa okunamadı: {url}"
        )
        print(
            f"[Page Reader] Hata: {e}"
        )

        return ""