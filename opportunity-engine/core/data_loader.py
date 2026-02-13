from __future__ import annotations

from dataclasses import dataclass
from typing import Dict

import pandas as pd

REQUIRED_SHEETS = ["Customers", "Accounts", "Events"]
OPTIONAL_SHEETS = ["Tasks"]

REQUIRED_COLUMNS = {
    "Customers": [
        "CustomerId",
        "FullName",
        "BirthDate",
        "Phone",
        "Email",
        "City",
        "MaritalStatus",
        "ChildrenCount",
        "EmploymentStatus",
    ],
    "Accounts": [
        "AccountId",
        "CustomerId",
        "ManagingEntity",
        "ProductType",
        "AccountStatus",
        "JoinDate",
        "BalanceNIS",
        "MgmtFeeFromBalancePct",
        "MgmtFeeFromDepositPct",
        "AgentName",
        "BusinessManager",
    ],
    "Events": [
        "EventId",
        "EventType",
        "EventStatus",
        "EventDate",
        "ExpectedDate",
        "CustomerId",
        "AccountId",
        "ManagingEntity",
        "ProductType",
        "AmountNIS",
        "BalanceSnapshotNIS",
        "Reason",
    ],
}

DATE_COLUMNS = {
    "Customers": ["BirthDate"],
    "Accounts": ["JoinDate"],
    "Events": ["EventDate", "ExpectedDate"],
}

ID_COLUMNS = {
    "Customers": ["CustomerId"],
    "Accounts": ["AccountId", "CustomerId"],
    "Events": ["EventId", "CustomerId", "AccountId"],
}


@dataclass
class LoadedData:
    customers: pd.DataFrame
    accounts: pd.DataFrame
    events: pd.DataFrame
    tasks: pd.DataFrame
    quality: Dict[str, float]


class DataValidationError(ValueError):
    pass


def _ensure_columns(df: pd.DataFrame, sheet: str) -> None:
    missing = [c for c in REQUIRED_COLUMNS[sheet] if c not in df.columns]
    if missing:
        raise DataValidationError(f"Missing columns in {sheet}: {missing}")


def _coerce_dates(df: pd.DataFrame, sheet: str) -> pd.DataFrame:
    for c in DATE_COLUMNS.get(sheet, []):
        df[c] = pd.to_datetime(df[c], errors="coerce")
    return df


def _coerce_ids(df: pd.DataFrame, sheet: str) -> pd.DataFrame:
    for c in ID_COLUMNS.get(sheet, []):
        df[c] = df[c].astype("string").fillna("")
    return df


def _quality_metrics(customers: pd.DataFrame, accounts: pd.DataFrame, events: pd.DataFrame) -> Dict[str, float]:
    critical_cols = ["CustomerId", "AccountId", "EventId", "EventType", "EventDate"]
    total_rows = len(customers) + len(accounts) + len(events)
    missing_vals = 0
    for df in [customers, accounts, events]:
        local_cols = [c for c in critical_cols if c in df.columns]
        if local_cols:
            missing_vals += int(df[local_cols].isna().sum().sum())

    events_without_account = int(events[events["AccountId"].isin(["", "<NA>"])].shape[0])
    accounts_without_customer = int(accounts[~accounts["CustomerId"].isin(customers["CustomerId"])].shape[0])

    duplicates = {
        "duplicate_customers": int(customers["CustomerId"].duplicated().sum()),
        "duplicate_accounts": int(accounts["AccountId"].duplicated().sum()),
        "duplicate_events": int(events["EventId"].duplicated().sum()),
    }

    return {
        "missing_ratio_pct": round((missing_vals / max(total_rows, 1)) * 100, 2),
        "events_without_account": events_without_account,
        "accounts_without_customer": accounts_without_customer,
        **duplicates,
    }


def load_excel(file_path: str) -> LoadedData:
    excel = pd.ExcelFile(file_path)
    sheet_names = excel.sheet_names

    missing_sheets = [s for s in REQUIRED_SHEETS if s not in sheet_names]
    if missing_sheets:
        raise DataValidationError(f"Missing required sheets: {missing_sheets}")

    frames = {}
    for sheet in REQUIRED_SHEETS + OPTIONAL_SHEETS:
        if sheet in sheet_names:
            df = pd.read_excel(file_path, sheet_name=sheet)
        else:
            df = pd.DataFrame()
        if sheet in REQUIRED_SHEETS:
            _ensure_columns(df, sheet)
            df = _coerce_dates(df, sheet)
            df = _coerce_ids(df, sheet)
        frames[sheet] = df

    quality = _quality_metrics(frames["Customers"], frames["Accounts"], frames["Events"])

    tasks = frames["Tasks"]
    if tasks.empty:
        tasks = pd.DataFrame()

    return LoadedData(
        customers=frames["Customers"],
        accounts=frames["Accounts"],
        events=frames["Events"],
        tasks=tasks,
        quality=quality,
    )
