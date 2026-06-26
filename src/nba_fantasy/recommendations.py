"""
Recommendation scoring helpers.

This module adds simple decision labels and confidence tiers to fantasy
basketball add/drop recommendations.
"""

from __future__ import annotations

import pandas as pd


def classify_recommendation(score: float) -> str:
    """
    Convert a combined add/drop score into a recommendation tier.
    """
    if score >= 5:
        return "Strong add"
    if score >= 2:
        return "Moderate add"
    if score >= 0:
        return "Marginal add"
    return "Avoid"


def classify_confidence(row: pd.Series) -> str:
    """
    Assign a simple confidence label.

    Current MVP logic:
    - Injured/GTD adds lower confidence.
    - Larger positive scores increase confidence.
    """
    score = row.get("combined_add_drop_score", 0)
    add_status = str(row.get("status_add", "")).upper()
    drop_status = str(row.get("status_drop", "")).upper()

    has_add_injury_flag = any(flag in add_status for flag in ["GTD", "O", "IR", "IL"])
    has_drop_injury_flag = any(flag in drop_status for flag in ["GTD", "O", "IR", "IL"])

    if score >= 5 and not has_add_injury_flag:
        return "High"

    if score >= 2 and not has_add_injury_flag:
        return "Medium"

    if score >= 2 and has_drop_injury_flag:
        return "Medium"

    return "Low"


def add_recommendation_labels(recommendations: pd.DataFrame) -> pd.DataFrame:
    """
    Add recommendation tier and confidence label columns.
    """
    out = recommendations.copy()

    out["recommendation_tier"] = out["combined_add_drop_score"].apply(
        classify_recommendation
    )

    out["confidence"] = out.apply(classify_confidence, axis=1)

    return out.sort_values(
        ["combined_add_drop_score", "value_delta", "category_fit_score"],
        ascending=False,
    ).reset_index(drop=True)