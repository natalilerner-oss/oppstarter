from __future__ import annotations

import pandas as pd


def _base_rule_output(event: pd.Series) -> dict:
    return {
        "EventId": event.get("EventId"),
        "CustomerId": event.get("CustomerId"),
        "AccountId": event.get("AccountId"),
        "EventType": event.get("EventType"),
        "EventStatus": event.get("EventStatus"),
        "ExpectedDate": event.get("ExpectedDate"),
        "AmountNIS": event.get("AmountNIS", 0),
        "ManagingEntity": event.get("ManagingEntity", ""),
        "ProductType": event.get("ProductType", ""),
        "Reason": event.get("Reason", ""),
    }


def events_to_tasks(events: pd.DataFrame, customers: pd.DataFrame, accounts: pd.DataFrame) -> pd.DataFrame:
    tasks: list[dict] = []

    for _, e in events.iterrows():
        etype = str(e.get("EventType", ""))
        status = str(e.get("EventStatus", "")).lower()
        task = _base_rule_output(e)

        if etype == "TransferOut" and status in {"new", "in_progress", "pending"}:
            task.update(
                {
                    "Category": "Retention",
                    "RecommendedActions": "שיחת שימור מיידית, בדיקת דמי ניהול והצעת חלופה",
                    "Confidence": "High",
                    "Rationale": "זוהתה דליפה פוטנציאלית מהתיק",
                }
            )
            tasks.append(task)

        elif etype == "Withdrawal" and status in {"new", "in_progress", "pending"}:
            task.update(
                {
                    "Category": "Retention",
                    "RecommendedActions": "בדיקת צורך כספי והצעת הלוואה במקום משיכה",
                    "Confidence": "High",
                    "Rationale": "משיכה בתהליך פוגעת בצבירה ארוכת טווח",
                }
            )
            tasks.append(task)

        elif etype in {"Reject", "FailedCharge"}:
            task.update(
                {
                    "Category": "Service",
                    "RecommendedActions": "טיפול בתקלה, יצירת קשר ועדכון פרטי חיוב",
                    "Confidence": "High",
                    "Rationale": f"אירוע שירות דורש טיפול. סיבה: {e.get('Reason', 'לא צוינה')}",
                }
            )
            tasks.append(task)

        elif etype == "LoanMaturity":
            task.update(
                {
                    "Category": "Sales",
                    "RecommendedActions": "הצעת מחזור או ניוד הלוואה",
                    "Confidence": "Medium",
                    "Rationale": "הלוואה עומדת לפירעון בקרוב",
                }
            )
            tasks.append(task)

        elif etype == "MgmtFeeIncrease":
            task.update(
                {
                    "Category": "Retention",
                    "RecommendedActions": "בחינת הורדת דמי ניהול או מעבר מסלול",
                    "Confidence": "Medium",
                    "Rationale": "עלייה יחסית בדמי ניהול מול התיק",
                }
            )
            tasks.append(task)

    # Hypothetical child-related opportunities when no explicit event exists
    for _, c in customers.iterrows():
        children = int(c.get("ChildrenCount", 0) or 0)
        age = (pd.Timestamp.today() - pd.to_datetime(c.get("BirthDate"), errors="coerce")).days // 365
        if 0 <= age <= 50 and children >= 1:
            task = {
                "EventId": f"HYP-{c.get('CustomerId')}",
                "CustomerId": c.get("CustomerId"),
                "AccountId": "",
                "EventType": "ChildBirth",
                "EventStatus": "new",
                "ExpectedDate": pd.Timestamp.today() + pd.Timedelta(days=30),
                "AmountNIS": 0,
                "ManagingEntity": "",
                "ProductType": "גמל להשקעה",
                "Reason": "זוהתה משפחה עם ילדים",
                "Category": "Sales",
                "RecommendedActions": "הצעה לפתיחת קופת גמל להשקעה לילד",
                "Confidence": "Low",
                "Rationale": "הזדמנות היפותטית מבוססת פרופיל משפחתי",
            }
            tasks.append(task)

    if not tasks:
        return pd.DataFrame()
    return pd.DataFrame(tasks).drop_duplicates(subset=["EventId", "CustomerId", "Category"])
