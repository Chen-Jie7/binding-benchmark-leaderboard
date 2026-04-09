import pandas as pd
import streamlit as st

from core.storage import load_submissions

st.title("Leaderboard")

submissions = load_submissions()

if not submissions:
    st.info("No submissions yet. Be the first!")
else:
    df = pd.DataFrame(submissions)

    # Ensure numeric types (Google Sheets returns strings)
    for col in ["f1", "accuracy", "coverage_pct"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Truncate timestamp to date
    if "submitted_at" in df.columns:
        df["submitted_at"] = df["submitted_at"].astype(str).str[:10]

    df = df.sort_values("f1", ascending=False).reset_index(drop=True)
    df.insert(0, "Rank", range(1, len(df) + 1))

    display_cols = ["Rank", "model_name", "f1", "accuracy", "coverage_pct", "submitted_at", "description"]
    display_cols = [c for c in display_cols if c in df.columns]

    st.dataframe(
        df[display_cols],
        use_container_width=True,
        hide_index=True,
        column_config={
            "Rank": st.column_config.NumberColumn("Rank", width="small"),
            "model_name": st.column_config.TextColumn("Model"),
            "f1": st.column_config.NumberColumn("F1 Score", format="%.4f"),
            "accuracy": st.column_config.NumberColumn("Accuracy", format="%.4f"),
            "coverage_pct": st.column_config.NumberColumn("Coverage %", format="%.1f%%"),
            "submitted_at": st.column_config.TextColumn("Date"),
            "description": st.column_config.TextColumn("Description", width="large"),
        },
    )
