from __future__ import annotations

import time
from typing import Optional

import requests

from core.config import settings
from core.security import redact_pii


class AIClient:
    def __init__(self) -> None:
        self.enabled = settings.ai_enabled and bool(settings.gemini_api_key)

    def summarize(self, context: str) -> Optional[str]:
        if not self.enabled:
            return None

        prompt = redact_pii(context)
        url = f"{settings.ai_base_url}/models/{settings.gemini_model}:generateContent?key={settings.gemini_api_key}"
        payload = {"contents": [{"parts": [{"text": prompt}]}]}

        for attempt in range(settings.ai_max_retries):
            try:
                response = requests.post(url, json=payload, timeout=settings.ai_timeout_seconds)
                response.raise_for_status()
                data = response.json()
                return (
                    data.get("candidates", [{}])[0]
                    .get("content", {})
                    .get("parts", [{}])[0]
                    .get("text", "")
                )
            except requests.RequestException:
                if attempt == settings.ai_max_retries - 1:
                    return "AI לא זמין כרגע, מוצגת תצוגת ברירת מחדל."
                time.sleep(2**attempt)
        return None
