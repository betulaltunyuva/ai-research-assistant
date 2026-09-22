from utils.text_chunker import chunk_text


def test_chunk_text():
    text = (
        "Bu birinci cümledir. "
        "Bu ikinci cümledir. "
        "Bu üçüncü cümledir. "
        "Bu dördüncü cümledir. "
        "Bu beşinci cümledir. "
    ) * 8

    chunks = chunk_text(
        text,
        chunk_size=120,
        overlap=20
    )

    assert isinstance(
        chunks,
        list
    )

    assert len(chunks) > 1

    assert all(
        isinstance(chunk, str)
        for chunk in chunks
    )

    assert all(
        chunk.strip()
        for chunk in chunks
    )


def test_empty_text():
    chunks = chunk_text(
        "",
        chunk_size=100,
        overlap=20
    )

    assert chunks == []