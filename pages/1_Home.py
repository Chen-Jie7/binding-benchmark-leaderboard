import streamlit as st

st.title("Protein-Ligand Binding Prediction Benchmark")

st.markdown("""
**Task**: Given a protein sequence and a small molecule (SMILES), predict whether they bind.

This benchmark contains **83,727** experimentally validated protein-compound pairs
from 20 data sources spanning multiple biophysical assay types.
""")

col1, col2, col3 = st.columns(3)
col1.metric("Total Pairs", "83,727")
col2.metric("Binders (positive)", "2,832 (3.4%)")
col3.metric("Non-binders (negative)", "80,895 (96.6%)")

st.markdown("---")

st.subheader("Assay Types")
st.markdown("""
| Assay | Count | % |
|-------|------:|--:|
| SPR (Surface Plasmon Resonance) | 34,358 | 41.0% |
| Fluorescence Polarization | 17,247 | 20.6% |
| BLI (Biolayer Interferometry) | 16,466 | 19.7% |
| Yeast Display | 13,540 | 16.2% |
| ITC (Isothermal Titration Calorimetry) | 2,116 | 2.5% |
""")

st.markdown("---")

st.subheader("Submission Format")
st.markdown("""
Upload a CSV file with three columns:

| Column | Type | Description |
|--------|------|-------------|
| `sequence` | string | Protein amino acid sequence (must exactly match `primary_molecule` in the benchmark) |
| `smiles` | string | Compound SMILES string (must exactly match `target_molecule` in the benchmark) |
| `binding_label` | int | Your prediction: `1` = binds, `0` = does not bind |

**Important**: Use the exact sequence and SMILES strings from the downloaded benchmark file.
Partial submissions are accepted (you don't have to predict all 83,727 pairs).
""")

st.markdown("---")

st.subheader("Evaluation Metrics")
st.markdown("""
- **F1 Score** (primary ranking metric): Harmonic mean of precision and recall for the
  positive class (binders). This is the most meaningful metric given the 96.6% negative
  class imbalance --- a naive all-negative predictor scores 0.0 F1.
- **Accuracy**: Fraction of correct predictions across all pairs.
""")
