import abc
import os
from typing import Any, Dict, List

import requests


class OCRBackend(abc.ABC):
    @abc.abstractmethod
    def recognize(self, image_bytes: bytes) -> List[Dict[str, Any]]:
        """Recognize text from image bytes and return structured result."""
        raise NotImplementedError


class BaiduUnlimitedOCRBackend(OCRBackend):
    def __init__(self, api_key: str | None = None, api_url: str | None = None):
        self.api_key = api_key or os.environ.get("BAIDU_OCR_API_KEY")
        self.api_url = api_url or os.environ.get("BAIDU_OCR_API_URL")
        if not self.api_key or not self.api_url:
            raise ValueError("Baidu OCR backend requires BAIDU_OCR_API_KEY and BAIDU_OCR_API_URL.")

    def recognize(self, image_bytes: bytes) -> List[Dict[str, Any]]:
        response = requests.post(
            self.api_url,
            headers={"Authorization": f"Bearer {self.api_key}"},
            files={"image": ("image.png", image_bytes, "image/png")},
            timeout=60,
        )
        response.raise_for_status()
        payload = response.json()
        return payload.get("results", [])
