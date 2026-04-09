from __future__ import annotations

import gspread
import streamlit as st

COLUMNS = [
    "id", "model_name", "description", "submitted_at",
    "f1", "accuracy", "n_matched", "n_total_gt", "coverage_pct",
]


@st.cache_resource
def _get_sheet() -> gspread.Worksheet:
    """Connect to the Google Sheet using service account credentials from secrets."""
    creds = dict(st.secrets["gcp_service_account"])
    gc = gspread.service_account_from_dict(creds)
    sh = gc.open(st.secrets["sheet_name"])
    ws = sh.sheet1

    # Ensure header row exists
    existing = ws.row_values(1)
    if not existing:
        ws.append_row(COLUMNS, value_input_option="RAW")

    return ws


def load_submissions() -> list[dict]:
    """Load all submissions from the Google Sheet."""
    ws = _get_sheet()
    records = ws.get_all_records()
    return records


def save_submission(entry: dict) -> None:
    """Append a submission row to the Google Sheet."""
    ws = _get_sheet()
    row = [entry.get(col, "") for col in COLUMNS]
    ws.append_row(row, value_input_option="RAW")
