from __future__ import annotations

import logging

import pandas as pd

from core.scoring import score_event, severity_from_score, sla_from_severity

logger = logging.getLogger(__name__)

DATE_CANDIDATE_COLUMNS = [
    "ExpectedDate",
    "DueDate",
    "Deadline",
    "Due",
    "expected_date",
    "due_date",
    "תאריך",
    "תאריך יעד",
    "תאריך_יעד",
]


def build_opportunities(tasks: pd.DataFrame) -> pd.DataFrame:
    if tasks.empty:
        return pd.DataFrame()

    out = tasks.copy()
    out["PriorityScore"] = out.apply(score_event, axis=1)
    out["Severity"] = out.apply(
        lambda r: severity_from_score(str(r.get("Category", "Service")), int(r.get("PriorityScore", 0))),
        axis=1,
    )
    out["SLA_Days"] = out["Severity"].map(sla_from_severity)
    today = pd.Timestamp.today()
    detected_date_column = next((col for col in DATE_CANDIDATE_COLUMNS if col in out.columns), None)

    if detected_date_column:
        out["Deadline"] = pd.to_datetime(out[detected_date_column], errors="coerce").fillna(today)
    else:
        logger.warning(
            "No supported date column found in tasks. Expected one of %s. Falling back to today's date.",
            DATE_CANDIDATE_COLUMNS,
        )
        out["Deadline"] = pd.Series(today, index=out.index)

    out["IsLate"] = out["Deadline"].dt.date < pd.Timestamp.today().date()
    return out.sort_values(by=["PriorityScore", "Deadline"], ascending=[False, True])
