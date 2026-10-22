from fastapi.testclient import TestClient

import api


client = TestClient(api.api)


def test_upload_within_limit_is_saved(monkeypatch):
    monkeypatch.setattr(api, "MAX_UPLOAD_SIZE_BYTES", 10)

    response = client.post(
        "/upload",
        files={"file": ("test_upload_small.txt", b"kucuk", "text/plain")}
    )

    file_path = api.UPLOAD_DIR / "test_upload_small.txt"

    try:
        assert response.status_code == 200
        assert file_path.read_bytes() == b"kucuk"

    finally:
        file_path.unlink(missing_ok=True)


def test_upload_over_limit_is_rejected(monkeypatch):
    monkeypatch.setattr(api, "MAX_UPLOAD_SIZE_BYTES", 10)

    response = client.post(
        "/upload",
        files={"file": ("test_upload_big.txt", b"x" * 11, "text/plain")}
    )

    assert response.status_code == 413
    assert not (api.UPLOAD_DIR / "test_upload_big.txt").exists()
