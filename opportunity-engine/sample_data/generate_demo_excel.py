from __future__ import annotations

from pathlib import Path

import pandas as pd


OUTPUT = Path(__file__).resolve().parent / "demo_portfolio.xlsx"


def main() -> None:
    customers = pd.DataFrame(
        [
            {
                "CustomerId": "123456782",
                "FullName": "נועם כהן",
                "BirthDate": "1989-04-10",
                "Phone": "0501112233",
                "Email": "noam@example.co.il",
                "City": "תל אביב",
                "MaritalStatus": "נשוי",
                "ChildrenCount": 2,
                "EmploymentStatus": "שכיר",
            },
            {
                "CustomerId": "223456782",
                "FullName": "מאיה לוי",
                "BirthDate": "1978-11-03",
                "Phone": "0523334455",
                "Email": "maya@example.co.il",
                "City": "חיפה",
                "MaritalStatus": "נשואה",
                "ChildrenCount": 1,
                "EmploymentStatus": "עצמאית",
            },
            {
                "CustomerId": "323456782",
                "FullName": "דניאל ישראלי",
                "BirthDate": "1995-02-18",
                "Phone": "0537654321",
                "Email": "daniel@example.co.il",
                "City": "באר שבע",
                "MaritalStatus": "רווק",
                "ChildrenCount": 0,
                "EmploymentStatus": "שכיר",
            },
        ]
    )

    accounts = pd.DataFrame(
        [
            {
                "AccountId": "ACC-1001",
                "CustomerId": "123456782",
                "ManagingEntity": "הראל",
                "ProductType": "קרן פנסיה",
                "AccountStatus": "Active",
                "JoinDate": "2016-01-01",
                "BalanceNIS": 420000,
                "MgmtFeeFromBalancePct": 0.65,
                "MgmtFeeFromDepositPct": 2.5,
                "AgentName": "אייל סוכן",
                "BusinessManager": "רן מנהל",
            },
            {
                "AccountId": "ACC-1002",
                "CustomerId": "223456782",
                "ManagingEntity": "מנורה",
                "ProductType": "קופת גמל",
                "AccountStatus": "Active",
                "JoinDate": "2018-05-10",
                "BalanceNIS": 210000,
                "MgmtFeeFromBalancePct": 0.9,
                "MgmtFeeFromDepositPct": 3.2,
                "AgentName": "אייל סוכן",
                "BusinessManager": "רן מנהל",
            },
        ]
    )

    events = pd.DataFrame(
        [
            {
                "EventId": "E-1",
                "EventType": "TransferOut",
                "EventStatus": "new",
                "EventDate": "2026-01-10",
                "ExpectedDate": "2026-01-14",
                "CustomerId": "123456782",
                "AccountId": "ACC-1001",
                "ManagingEntity": "הראל",
                "ProductType": "קרן פנסיה",
                "AmountNIS": 150000,
                "BalanceSnapshotNIS": 420000,
                "Reason": "מעבר לגוף אחר",
            },
            {
                "EventId": "E-2",
                "EventType": "Withdrawal",
                "EventStatus": "in_progress",
                "EventDate": "2026-01-09",
                "ExpectedDate": "2026-01-12",
                "CustomerId": "223456782",
                "AccountId": "ACC-1002",
                "ManagingEntity": "מנורה",
                "ProductType": "קופת גמל",
                "AmountNIS": 50000,
                "BalanceSnapshotNIS": 210000,
                "Reason": "צורך תזרימי",
            },
            {
                "EventId": "E-3",
                "EventType": "Reject",
                "EventStatus": "new",
                "EventDate": "2026-01-08",
                "ExpectedDate": "2026-01-09",
                "CustomerId": "323456782",
                "AccountId": "",
                "ManagingEntity": "הפניקס",
                "ProductType": "ביטוח מנהלים",
                "AmountNIS": 0,
                "BalanceSnapshotNIS": 90000,
                "Reason": "שגיאת בנק",
            },
        ]
    )

    with pd.ExcelWriter(OUTPUT, engine="openpyxl") as writer:
        customers.to_excel(writer, sheet_name="Customers", index=False)
        accounts.to_excel(writer, sheet_name="Accounts", index=False)
        events.to_excel(writer, sheet_name="Events", index=False)

    print(f"Demo file created: {OUTPUT}")


if __name__ == "__main__":
    main()
