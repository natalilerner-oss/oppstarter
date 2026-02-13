import pandas as pd

from core.rules import events_to_tasks


def test_rules_transfer_withdraw_reject():
    events = pd.DataFrame(
        [
            {"EventId": "1", "CustomerId": "123", "AccountId": "A1", "EventType": "TransferOut", "EventStatus": "new", "ExpectedDate": "2026-01-01", "AmountNIS": 1000, "ManagingEntity": "X", "ProductType": "Y", "Reason": ""},
            {"EventId": "2", "CustomerId": "123", "AccountId": "A1", "EventType": "Withdrawal", "EventStatus": "in_progress", "ExpectedDate": "2026-01-01", "AmountNIS": 1000, "ManagingEntity": "X", "ProductType": "Y", "Reason": ""},
            {"EventId": "3", "CustomerId": "123", "AccountId": "A1", "EventType": "Reject", "EventStatus": "new", "ExpectedDate": "2026-01-01", "AmountNIS": 0, "ManagingEntity": "X", "ProductType": "Y", "Reason": "err"},
        ]
    )
    customers = pd.DataFrame([{"CustomerId": "123", "BirthDate": "1990-01-01", "ChildrenCount": 0}])
    accounts = pd.DataFrame([{"AccountId": "A1", "CustomerId": "123"}])

    tasks = events_to_tasks(events, customers, accounts)
    categories = tasks.set_index("EventType")["Category"].to_dict()

    assert categories["TransferOut"] == "Retention"
    assert categories["Withdrawal"] == "Retention"
    assert categories["Reject"] == "Service"
