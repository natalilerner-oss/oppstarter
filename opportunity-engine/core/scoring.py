from __future__ import annotations

from datetime import datetime

import pandas as pd

EVENT_BOOST = {
    "TransferOut": 40,
    "Withdrawal": 30,
    "Reject": 22,
    "LoanMaturity": 24,
    "MgmtFeeIncrease": 20,
    "FailedCharge": 18,
    "DepositDrop": 20,
    "ChildBirth": 16,
}


def _urgency_points(expected_date: pd.Timestamp | None, now: pd.Timestamp) -> int:
    if pd.isna(expected_date):
        return 5
    delta_days = (expected_date.date() - now.date()).days
    if delta_days <= 0:
        return 25
    if delta_days <= 7:
        return 20
    if delta_days <= 30:
        return 12
    return 4


def score_event(event: pd.Series, now: pd.Timestamp | None = None) -> int:
    now = now or pd.Timestamp(datetime.utcnow())
    event_type = str(event.get("EventType", ""))
    status = str(event.get("EventStatus", ""))
    amount = float(event.get("AmountNIS", 0) or 0)
    balance = float(event.get("BalanceSnapshotNIS", 0) or 0)
    expected = event.get("ExpectedDate", pd.NaT)

    base = EVENT_BOOST.get(event_type, 10)
    value = min(25, int((amount / 5000) + (balance / 200000) * 10))
    urgency = _urgency_points(expected, now)
    done_penalty = -20 if status.lower() in {"completed", "closed", "done"} else 0
    total = max(0, min(100, base + value + urgency + done_penalty))
    return int(total)


def severity_from_score(category: str, score: int) -> str:
    if category == "Retention" and score >= 70:
        return "CRITICAL"
    if score >= 75:
        return "CRITICAL"
    if score >= 55:
        return "HIGH"
    if score >= 35:
        return "MEDIUM"
    return "LOW"


def sla_from_severity(severity: str) -> int:
    mapping = {"CRITICAL": 1, "HIGH": 3, "MEDIUM": 7, "LOW": 14}
    return mapping.get(severity, 7)
