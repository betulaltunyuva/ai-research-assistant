import pytest
from fastapi import HTTPException

from api import (
    ResearchRequest,
    UPLOAD_DIR,
    validate_research_request
)


def make_request(document_path):
    return ResearchRequest(
        query="Test konusu",
        document_path=document_path
    )


def test_uploaded_document_is_accepted():
    file_path = UPLOAD_DIR / "test_document_path.txt"
    file_path.write_text("test", encoding="utf-8")

    try:
        _, _, document_path = validate_research_request(
            make_request(str(file_path))
        )

        assert document_path == str(file_path)

    finally:
        file_path.unlink()


def test_document_outside_upload_dir_is_rejected():
    with pytest.raises(HTTPException) as error:
        validate_research_request(
            make_request("api.py")
        )

    assert error.value.status_code == 400


def test_path_traversal_is_rejected():
    with pytest.raises(HTTPException) as error:
        validate_research_request(
            make_request(
                str(UPLOAD_DIR / ".." / ".." / "api.py")
            )
        )

    assert error.value.status_code == 400


def test_missing_uploaded_document_returns_404():
    with pytest.raises(HTTPException) as error:
        validate_research_request(
            make_request(
                str(UPLOAD_DIR / "olmayan_dosya.pdf")
            )
        )

    assert error.value.status_code == 404
