from __future__ import annotations

from pathlib import Path

import pandas as pd
import streamlit as st

PARQUET_PATH = Path(__file__).parent.parent / "small_molecule_benchmark.parquet"
KEY_SEP = "|||"


@st.cache_data
def load_ground_truth() -> pd.DataFrame:
    """Load benchmark parquet and build a lookup key for matching."""
    df = pd.read_parquet(
        PARQUET_PATH,
        columns=["primary_molecule", "target_molecule", "binding_label"],
    )
    df["_key"] = df["primary_molecule"] + KEY_SEP + df["target_molecule"]
    return df


def get_parquet_bytes() -> bytes:
    """Read the raw parquet file bytes for the download button."""
    return PARQUET_PATH.read_bytes()
