import pandas as pd

from core.scoring import score_event


def test_scoring_is_deterministic():
    event = pd.Series(
        {
            "EventType": "TransferOut",
            "EventStatus": "new",
            "AmountNIS": 100000,
            "BalanceSnapshotNIS": 500000,
            "ExpectedDate": pd.Timestamp("2026-01-10"),
        }
    )
    now = pd.Timestamp("2026-01-01")
    s1 = score_event(event, now=now)
    s2 = score_event(event, now=now)
    assert s1 == s2
    assert 0 <= s1 <= 100
