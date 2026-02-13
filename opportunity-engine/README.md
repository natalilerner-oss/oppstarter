# מנוע-הזדמנויות (MVP)

אפליקציית Streamlit לניתוח תיק ביטוח/פנסיה, זיהוי אירועים, והמרתם להזדמנויות מכירה/שימור/שירות עם דירוג עדיפות, SLA והמלצת פעולה.

## יכולות עיקריות
- טעינת Excel עם הטאבים: `Customers`, `Accounts`, `Events` (ו-`Tasks` אופציונלי).
- Rules Engine ליצירת משימות אוטומטיות מאירועים.
- Scoring דטרמיניסטי 0-100 + Severity + SLA.
- Dashboard בעברית RTL:
  - סקירה כללית + KPI + פילוח מוצר + הזדמנויות אחרונות.
  - מסך הזדמנויות עם פילטרים, כרטיסים והורדת CSV.
  - מסך תיק לקוח (Customer 360).
- Data Quality Panel בסיידבר.
- שכבת AI אופציונלית (Gemini) עם timeout/retry/backoff ו-fallback בטוח.
- Redaction ל-PII לפני פנייה ל-AI.

## התקנה והרצה
```bash
cd opportunity-engine
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## קונפיגורציה
העתק ` .env.example` ל-`.env` ועדכן במידת הצורך:
- `AI_ENABLED=true`
- `GEMINI_API_KEY=...`

## פורמט קובץ קלט
- `Customers`: `CustomerId, FullName, BirthDate, Phone, Email, City, MaritalStatus, ChildrenCount, EmploymentStatus`
- `Accounts`: `AccountId, CustomerId, ManagingEntity, ProductType, AccountStatus, JoinDate, BalanceNIS, MgmtFeeFromBalancePct, MgmtFeeFromDepositPct, AgentName, BusinessManager`
- `Events`: `EventId, EventType, EventStatus, EventDate, ExpectedDate, CustomerId, AccountId, ManagingEntity, ProductType, AmountNIS, BalanceSnapshotNIS, Reason`
- `Tasks` (אופציונלי)

## בדיקות
```bash
pytest
```

## דמו דאטה
```bash
python sample_data/generate_demo_excel.py
```
# opportunity-engine

Scaffold directory created for the opportunity engine workspace.
