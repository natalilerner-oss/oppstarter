from __future__ import annotations


def render_quality_text(quality: dict) -> str:
    return (
        f"חסרים בשדות קריטיים: {quality.get('missing_ratio_pct', 0)}% | "
        f"אירועים ללא חשבון: {quality.get('events_without_account', 0)} | "
        f"חשבונות ללא לקוח: {quality.get('accounts_without_customer', 0)}"
    )
