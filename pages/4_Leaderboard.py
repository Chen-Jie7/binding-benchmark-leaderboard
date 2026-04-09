import pandas as pd
import streamlit as st

from core.storage import load_submissions

st.title("Leaderboard")

submissions = load_submissions()

if not submissions:
    st.info("No submissions yet. Be the first!")
else:
    rows = []
    for s in submissions:
        rows.append({
            "model_name": s["model_name"],
            "f1": s["metrics"]["f1"],
            "accuracy": s["metrics"]["accuracy"],
            "coverage_pct": s["coverage_pct"],
            "submitted_at": s["submitted_at"][:10],
            "description": s.get("description", ""),
        })

    df = pd.DataFrame(rows)
    df = df.sort_values("f1", ascending=False).reset_index(drop=True)
    df.insert(0, "Rank", range(1, len(df) + 1))

    st.dataframe(
        df,
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
