from __future__ import annotations

import pandas as pd

from core.scoring import score_event, severity_from_score, sla_from_severity


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
    out["Deadline"] = pd.to_datetime(out["ExpectedDate"], errors="coerce").fillna(pd.Timestamp.today())
    out["IsLate"] = out["Deadline"].dt.date < pd.Timestamp.today().date()
    return out.sort_values(by=["PriorityScore", "Deadline"], ascending=[False, True])
