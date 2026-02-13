from __future__ import annotations

import pandas as pd
import streamlit as st

from core.ai_client import AIClient
from core.data_loader import DataValidationError, load_excel
from core.opportunities import build_opportunities
from core.quality import render_quality_text
from core.rules import events_to_tasks

st.set_page_config(page_title="מנוע-הזדמנויות", layout="wide")
st.markdown(
    """
    <style>
      body, .stApp {direction: rtl; text-align: right;}
      .kpi {background: #f4f7fb; border-radius: 12px; padding: 12px;}
      .sev-critical {color: #c62828; font-weight:700;}
      .sev-high {color: #ef6c00; font-weight:700;}
      .sev-medium {color: #1565c0; font-weight:700;}
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("מנוע-הזדמנויות")
uploaded = st.file_uploader("העלה קובץ Excel", type=["xlsx"])

if not uploaded:
    st.info("יש להעלות קובץ Excel עם הטאבים Customers/Accounts/Events")
    st.stop()

with open("/tmp/uploaded.xlsx", "wb") as f:
    f.write(uploaded.getbuffer())

try:
    data = load_excel("/tmp/uploaded.xlsx")
except DataValidationError as e:
    st.error(f"שגיאת ולידציה: {e}")
    st.stop()

st.sidebar.subheader("Data Quality Panel")
st.sidebar.caption(render_quality_text(data.quality))

if data.tasks.empty:
    tasks = events_to_tasks(data.events, data.customers, data.accounts)
else:
    tasks = data.tasks

opps = build_opportunities(tasks)
merged = opps.merge(data.customers[["CustomerId", "FullName"]], on="CustomerId", how="left")

# Tabs
view = st.radio("ניווט", ["סקירה כללית", "הזדמנויות", "תיק לקוחות"], horizontal=True)

if view == "סקירה כללית":
    aum = float(data.accounts["BalanceNIS"].fillna(0).sum())
    active_customers = data.accounts[data.accounts["AccountStatus"].astype(str).str.lower() == "active"]["CustomerId"].nunique()
    hot = int((opps["Severity"].isin(["CRITICAL", "HIGH"])).sum()) if not opps.empty else 0
    avg_fee = float(data.accounts["MgmtFeeFromBalancePct"].fillna(0).mean())

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("AUM בניהול", f"₪{aum:,.0f}")
    c2.metric("לקוחות פעילים", int(active_customers))
    c3.metric("הזדמנויות חמות", hot)
    c4.metric("דמי ניהול ממוצעים", f"{avg_fee:.2f}%")

    st.subheader("פילוח תיק לפי מוצר")
    by_product = data.accounts.groupby("ProductType", dropna=False)["BalanceNIS"].sum().reset_index()
    st.bar_chart(by_product.set_index("ProductType"))

    st.subheader("הזדמנויות אחרונות שזוהו")
    cols = ["FullName", "EventType", "Category", "Severity", "PriorityScore", "RecommendedActions"]
    st.dataframe(merged[cols].head(5), use_container_width=True)

    ai = AIClient()
    if ai.enabled:
        summary = ai.summarize(f"סכם ב-3 שורות את מצב התיק: {merged.head(20).to_dict(orient='records')}")
        st.info(summary or "אין סיכום AI כרגע")

elif view == "הזדמנויות":
    st.subheader("Taskboard")
    df = merged.copy()

    col1, col2, col3 = st.columns(3)
    category = col1.selectbox("קטגוריה", ["הכל"] + sorted(df["Category"].dropna().unique().tolist()))
    entity = col2.selectbox("גוף מנהל", ["הכל"] + sorted(df["ManagingEntity"].dropna().astype(str).unique().tolist()))
    product = col3.selectbox("סוג מוצר", ["הכל"] + sorted(df["ProductType"].dropna().astype(str).unique().tolist()))

    col4, col5, col6 = st.columns(3)
    event_type = col4.selectbox("סוג אירוע", ["הכל"] + sorted(df["EventType"].dropna().astype(str).unique().tolist()))
    status = col5.selectbox("סטטוס משימה", ["הכל"] + sorted(df["EventStatus"].dropna().astype(str).unique().tolist()))
    min_score = col6.slider("מינימום PriorityScore", 0, 100, 0)

    late_only = st.checkbox("רק באיחור")
    search = st.text_input("חיפוש חופשי")

    if category != "הכל":
        df = df[df["Category"] == category]
    if entity != "הכל":
        df = df[df["ManagingEntity"].astype(str) == entity]
    if product != "הכל":
        df = df[df["ProductType"].astype(str) == product]
    if event_type != "הכל":
        df = df[df["EventType"].astype(str) == event_type]
    if status != "הכל":
        df = df[df["EventStatus"].astype(str) == status]

    df = df[df["PriorityScore"] >= min_score]
    if late_only:
        df = df[df["IsLate"]]
    if search:
        mask = df.astype(str).apply(lambda c: c.str.contains(search, case=False, na=False)).any(axis=1)
        df = df[mask]

    for _, row in df.iterrows():
        st.markdown(
            f"""
            ### {row.get('FullName', '')} | {row.get('CustomerId','')}
            **{row.get('ManagingEntity','')} / {row.get('ProductType','')}**  
            אירוע: {row.get('EventType','')} ({row.get('EventStatus','')}) | סכום: ₪{float(row.get('AmountNIS',0)):,.0f}  
            דדליין: {pd.to_datetime(row.get('Deadline')).date()} | עדיפות: {int(row.get('PriorityScore', 0))}  
            חומרה: **{row.get('Severity', '')}** | המלצה: {row.get('RecommendedActions', '')}
            """
        )
        st.divider()

    csv_data = df.to_csv(index=False).encode("utf-8-sig")
    st.download_button("הורדת CSV", data=csv_data, file_name="opportunities_filtered.csv", mime="text/csv")

else:
    st.subheader("תיק לקוחות")
    customer_id = st.selectbox("בחר לקוח לפי ת\"ז", sorted(data.customers["CustomerId"].dropna().astype(str).unique().tolist()))
    cust = data.customers[data.customers["CustomerId"].astype(str) == customer_id]

    if cust.empty:
        st.warning("לקוח לא נמצא")
    else:
        st.write("### פרטי לקוח")
        st.dataframe(cust, use_container_width=True)

        st.write("### מוצרים")
        st.dataframe(data.accounts[data.accounts["CustomerId"].astype(str) == customer_id], use_container_width=True)

        st.write("### אירועים אחרונים")
        cevents = data.events[data.events["CustomerId"].astype(str) == customer_id].sort_values("EventDate", ascending=False)
        st.dataframe(cevents.head(10), use_container_width=True)

        st.write("### משימות פתוחות")
        ctasks = merged[(merged["CustomerId"].astype(str) == customer_id) & (~merged["EventStatus"].astype(str).str.lower().isin(["completed", "closed", "done"]))]
        st.dataframe(ctasks, use_container_width=True)
