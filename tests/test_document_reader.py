from utils.document_reader import read_document


def test_txt_document_reader(tmp_path):
    test_file = tmp_path / "test_document.txt"

    test_text = (
        "AI Research Assistant "
        "belge okuma testi."
    )

    test_file.write_text(
        test_text,
        encoding="utf-8"
    )

    result = read_document(
        str(test_file)
    )

    assert result["file_name"] == "test_document.txt"
    assert result["file_type"] == "txt"
    assert test_text in result["text"]
    assert result["character_count"] > 0