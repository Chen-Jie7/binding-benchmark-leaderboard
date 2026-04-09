import streamlit as st

from core.data_loader import get_parquet_bytes, load_ground_truth

st.title("Download Benchmark Data")

st.markdown(
    "Download the full benchmark file containing **83,727** protein-ligand pairs "
    "with binding labels."
)

gt = load_ground_truth()

st.subheader("Preview (first 10 rows)")
preview = gt[["primary_molecule", "target_molecule", "binding_label"]].head(10)
st.dataframe(preview, use_container_width=True, hide_index=True)

st.markdown("---")

st.download_button(
    label="Download small_molecule_benchmark.parquet (10 MB)",
    data=get_parquet_bytes(),
    file_name="small_molecule_benchmark.parquet",
    mime="application/octet-stream",
)

st.markdown("""
**Columns in the file:**
- `primary_molecule` — protein sequence (use as `sequence` in your submission)
- `target_molecule` — compound SMILES (use as `smiles` in your submission)
- `binding_label` — ground truth: True (binds) / False (does not bind)
- Plus 22 additional metadata columns (assay type, confidence, structure info, etc.)
""")
