import pandas as pd
import pytest

from core.data_loader import DataValidationError, load_excel


def test_loader_fails_on_missing_required_sheet(tmp_path):
    path = tmp_path / "bad.xlsx"

    with pd.ExcelWriter(path, engine="openpyxl") as writer:
        pd.DataFrame([{"CustomerId": "1"}]).to_excel(writer, sheet_name="Customers", index=False)

    with pytest.raises(DataValidationError, match="Missing required sheets"):
        load_excel(str(path))
