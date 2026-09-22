def chunk_text(
    text: str,
    chunk_size: int = 1000,
    overlap: int = 150
) -> list[str]:

    text = text.strip()

    if not text:
        return []

    if chunk_size <= 0:
        raise ValueError(
            "chunk_size 0'dan büyük olmalıdır."
        )

    if overlap < 0 or overlap >= chunk_size:
        raise ValueError(
            "overlap, chunk_size değerinden küçük olmalıdır."
        )

    chunks = []
    start = 0

    while start < len(text):
        end = min(
            start + chunk_size,
            len(text)
        )

        # Metni mümkünse cümlenin veya paragrafın
        # ortasından kesmemeye çalış.
        if end < len(text):
            paragraph_break = text.rfind(
                "\n\n",
                start,
                end
            )

            sentence_break = text.rfind(
                ". ",
                start,
                end
            )

            best_break = max(
                paragraph_break,
                sentence_break
            )

            if best_break > start + (chunk_size // 2):
                end = best_break + 1

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        if end >= len(text):
            break

        start = end - overlap

    return chunks