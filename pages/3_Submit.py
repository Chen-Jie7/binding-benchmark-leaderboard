import uuid
from datetime import datetime, timezone

import pandas as pd
import streamlit as st

from core.data_loader import load_ground_truth
from core.evaluator import evaluate_submission, validate_submission
from core.storage import save_submission

st.title("Submit Predictions")

st.subheader("Expected CSV Format")
st.markdown(
    "Your CSV must have exactly three columns: `sequence`, `smiles`, and `binding_label`.\n\n"
    "- **sequence** must exactly match a `primary_molecule` value from the benchmark file\n"
    "- **smiles** must exactly match a `target_molecule` value from the benchmark file\n"
    "- **binding_label** is your model's prediction: `1` (binds) or `0` (does not bind)"
)

with st.expander("Show example CSV"):
    example_csv = (
        "sequence,smiles,binding_label\n"
        "SARIAKAKKLIYKLEKLWNARDNDGILKLFKDDAVFNLNGVPYKGKEAIK...,"
        "COc1ccc(-n2nc(C(=N)O)c3c2C(=O)N(c2ccc(N4CCCCC4=O)cc2)CC3)cc1,1\n"
        "PSEEEKEEILELINEFKEAFEAGDLETISKLFDDDFKFKSFNLSKEEFLE...,"
        "COc1ccc(-n2nc(C(=N)O)c3c2C(=O)N(c2ccc(N4CCCCC4=O)cc2)CC3)cc1,1\n"
        "DPDRHGRSLAEALLAGDRATLEAALDAARDEVARRHPELADALYEVSRAF...,"
        "CC(C)CN(C[C@@H](O)[C@H](Cc1ccccc1)N=C(O)O[C@H]1CCOC1)S(=O)(=O)c1ccc(N)cc1,0\n"
        "NPELIAELLEKGRRAAAEGSLEALAYYGLVALLYEVAGEPEKALEVLREG...,"
        "CC(C)CN(C[C@@H](O)[C@H](Cc1ccccc1)N=C(O)O[C@H]1CCOC1)S(=O)(=O)c1ccc(N)cc1,0\n"
    )
    st.code(example_csv, language="text")
    st.caption(
        "Sequences are truncated here for display. "
        "In your actual submission, use the **full** sequences and SMILES "
        "exactly as they appear in the downloaded benchmark file."
    )

st.markdown("---")

model_name = st.text_input(
    "Model Name *",
    max_chars=100,
    placeholder="e.g., BindPredict-v2",
)
description = st.text_area(
    "Model Description",
    max_chars=500,
    placeholder="Brief description of your approach...",
)

uploaded_file = st.file_uploader("Upload predictions CSV", type=["csv"])

if st.button("Submit", type="primary"):
    if not model_name.strip():
        st.error("Model name is required.")
    elif not uploaded_file:
        st.error("Please upload a CSV file.")
    else:
        try:
            sub_df = pd.read_csv(uploaded_file)
        except Exception as e:
            st.error(f"Failed to parse CSV: {e}")
            sub_df = None

        if sub_df is not None:
            errors = validate_submission(sub_df)
            if errors:
                for err in errors:
                    st.error(err)
            else:
                gt = load_ground_truth()
                try:
                    result = evaluate_submission(sub_df, gt)
                except ValueError as e:
                    st.error(str(e))
                    result = None

                if result is not None:
                    for w in result.warnings:
                        st.warning(w)

                    st.markdown("---")
                    st.subheader("Results")

                    col1, col2, col3 = st.columns(3)
                    col1.metric("F1 Score", f"{result.f1:.4f}")
                    col2.metric("Accuracy", f"{result.accuracy:.4f}")
                    col3.metric("Coverage", f"{result.coverage_pct}%")

                    entry = {
                        "id": uuid.uuid4().hex[:8],
                        "model_name": model_name.strip(),
                        "description": description.strip(),
                        "submitted_at": datetime.now(timezone.utc).isoformat(),
                        "metrics": {
                            "accuracy": result.accuracy,
                            "f1": result.f1,
                        },
                        "n_matched": result.n_matched,
                        "n_total_gt": result.n_total_gt,
                        "coverage_pct": result.coverage_pct,
                    }
                    save_submission(entry)
                    st.success(
                        f"Submission recorded! "
                        f"Check the **Leaderboard** to see your ranking."
                    )
