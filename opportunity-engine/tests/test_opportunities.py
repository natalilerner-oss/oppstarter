import pandas as pd

from core.opportunities import build_opportunities


def _base_task(**overrides):
    row = {
        "TaskId": "T1",
        "EventId": "E1",
        "CustomerId": "123",
        "AccountId": "A1",
        "Category": "Service",
        "PriorityScore": 55,
        "OwnerAgent": "Agent",
        "TaskStatus": "Open",
        "RecommendedActions": "Call",
    }
    row.update(overrides)
    return row


def test_build_opportunities_uses_due_date_when_expected_date_missing():
    tasks = pd.DataFrame([_base_task(DueDate="2026-01-15")])

    out = build_opportunities(tasks)

    assert not out.empty
    assert "Deadline" in out.columns
    assert pd.api.types.is_datetime64_any_dtype(out["Deadline"])
    assert out.iloc[0]["Deadline"].date() == pd.Timestamp("2026-01-15").date()


def test_build_opportunities_fallback_when_no_date_column(caplog):
    tasks = pd.DataFrame([_base_task()])

    with caplog.at_level("WARNING"):
        out = build_opportunities(tasks)

    assert not out.empty
    assert "Deadline" in out.columns
    assert pd.api.types.is_datetime64_any_dtype(out["Deadline"])
    assert out["Deadline"].notna().all()
    assert "No supported date column found in tasks" in caplog.text
