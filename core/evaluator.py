from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, f1_score

from .data_loader import KEY_SEP

REQUIRED_COLUMNS = {"sequence", "smiles", "binding_label"}


@dataclass
class EvaluationResult:
    accuracy: float
    f1: float
    n_matched: int
    n_total_gt: int
    coverage_pct: float
    n_unmatched_submission: int
    warnings: list[str]


def validate_submission(df: pd.DataFrame) -> list[str]:
    """Validate submission CSV format. Returns list of error messages (empty = valid)."""
    errors = []

    if df.empty:
        return ["Uploaded CSV is empty."]

    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        errors.append(f"Missing required columns: {', '.join(sorted(missing))}")
        return errors

    # Check binding_label values
    label_col = df["binding_label"]
    try:
        labels = pd.to_numeric(label_col, errors="raise")
    except (ValueError, TypeError):
        errors.append(
            "Column 'binding_label' must contain only 0 or 1. Found non-numeric values."
        )
        return errors

    invalid = labels[~labels.isin([0, 1])]
    if len(invalid) > 0:
        sample = invalid.head(5).tolist()
        errors.append(
            f"Column 'binding_label' must contain only 0 or 1. "
            f"Found invalid values: {sample}"
        )

    # Check for duplicate (sequence, smiles) pairs
    dup_mask = df.duplicated(subset=["sequence", "smiles"], keep=False)
    n_dups = dup_mask.sum()
    if n_dups > 0:
        errors.append(
            f"Found {n_dups} rows with duplicate (sequence, smiles) pairs. "
            f"Each pair must appear exactly once."
        )

    return errors


def evaluate_submission(
    submission_df: pd.DataFrame,
    ground_truth_df: pd.DataFrame,
) -> EvaluationResult:
    """Match submission against ground truth and compute metrics."""
    sub = submission_df.copy()
    sub["sequence"] = sub["sequence"].astype(str).str.strip()
    sub["smiles"] = sub["smiles"].astype(str).str.strip()
    sub["binding_label"] = pd.to_numeric(sub["binding_label"]).astype(int)
    sub["_key"] = sub["sequence"] + KEY_SEP + sub["smiles"]

    # Inner join on key
    merged = sub.merge(
        ground_truth_df[["_key", "binding_label"]],
        on="_key",
        suffixes=("_pred", "_true"),
    )

    n_matched = len(merged)
    n_total_gt = len(ground_truth_df)
    n_unmatched = len(sub) - n_matched

    warnings = []
    if n_matched == 0:
        raise ValueError(
            "No submission rows matched ground truth pairs. "
            "Check that 'sequence' and 'smiles' columns exactly match "
            "the benchmark data (primary_molecule and target_molecule)."
        )

    if n_unmatched > 0:
        warnings.append(
            f"{n_unmatched} rows in your submission had no matching ground truth pair "
            f"and were ignored."
        )

    coverage_pct = round(n_matched / n_total_gt * 100, 1)
    if coverage_pct < 100:
        warnings.append(
            f"Submission covers {n_matched:,}/{n_total_gt:,} pairs ({coverage_pct}%)."
        )

    y_true = merged["binding_label_true"].astype(int).values
    y_pred = merged["binding_label_pred"].values

    accuracy = float(accuracy_score(y_true, y_pred))
    f1 = float(f1_score(y_true, y_pred, zero_division=0.0))

    return EvaluationResult(
        accuracy=round(accuracy, 6),
        f1=round(f1, 6),
        n_matched=n_matched,
        n_total_gt=n_total_gt,
        coverage_pct=coverage_pct,
        n_unmatched_submission=n_unmatched,
        warnings=warnings,
    )
