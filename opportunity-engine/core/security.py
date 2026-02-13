from __future__ import annotations

import re


def redact_pii(text: str) -> str:
    if not text:
        return text
    redacted = re.sub(r"\b\d{9}\b", "[REDACTED_ID]", text)
    redacted = re.sub(r"\b0\d{8,9}\b", "[REDACTED_PHONE]", redacted)
    redacted = re.sub(r"[\w.+-]+@[\w-]+\.[\w.-]+", "[REDACTED_EMAIL]", redacted)
    return redacted
