import os
import types
from pathlib import Path

import pytest

from ocr_pipeline.backend import BaiduUnlimitedOCRBackend, OCRBackend


class DummyResponse:
    def __init__(self, payload):
        self._payload = payload

    def raise_for_status(self):
        pass

    def json(self):
        return self._payload


def test_baidu_backend_requires_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("BAIDU_OCR_API_KEY", raising=False)
    monkeypatch.delenv("BAIDU_OCR_API_URL", raising=False)
    with pytest.raises(ValueError):
        BaiduUnlimitedOCRBackend()


def test_baidu_backend_recognize(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("BAIDU_OCR_API_KEY", "test-key")
    monkeypatch.setenv("BAIDU_OCR_API_URL", "https://example.com/ocr")

    def fake_post(url: str, headers=None, files=None, timeout=None):
        assert url == "https://example.com/ocr"
        assert headers == {"Authorization": "Bearer test-key"}
        assert "image" in files
        return DummyResponse({"results": [{"text": "hello"}]})

    monkeypatch.setattr("ocr_pipeline.backend.requests.post", fake_post)
    backend = BaiduUnlimitedOCRBackend()
    result = backend.recognize(b"fake-image-bytes")
    assert result == [{"text": "hello"}]
