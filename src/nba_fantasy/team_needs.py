"""
Team category-need analysis.

This module estimates which 9-category fantasy basketball stats a roster is
strong or weak in, then uses those needs to evaluate add/drop decisions.
"""

from __future__ import annotations

import pandas as pd

CATEGORY_Z_COLUMNS = [
    "pts_z",
    "reb_z",
    "ast_z",
    "stl_z",
    "blk_z",
    "threes_z",
    "fg_impact_z",
    "ft_impact_z",
    "to_z",
]


def calculate_team_category_profile(
    ranked_roster: pd.DataFrame,
    category_z_columns: list[str] | None = None,
) -> pd.Series:
    """
    Sum category z-scores across rostered players.

    Positive values indicate roster strengths.
    Negative values indicate roster weaknesses.
    """
    if category_z_columns is None:
        category_z_columns = CATEGORY_Z_COLUMNS

    available_columns = [col for col in category_z_columns if col in ranked_roster.columns]

    return ranked_roster[available_columns].sum().sort_values()


def identify_weak_categories(
    team_profile: pd.Series,
    n: int = 3,
) -> list[str]:
    """
    Return the weakest category z-score columns.
    """
    return team_profile.sort_values(ascending=True).head(n).index.tolist()


def add_category_fit_score(
    recommendations: pd.DataFrame,
    weak_categories: list[str],
) -> pd.DataFrame:
    """
    Add a category-fit score to add/drop recommendations.

    For each weak category, compare the add player's category z-score against
    the drop player's category z-score.

    Positive values mean the add improves weak categories.
    """
    out = recommendations.copy()

    fit_components = []

    for category in weak_categories:
        add_col = f"{category}_add"
        drop_col = f"{category}_drop"

        if add_col in out.columns and drop_col in out.columns:
            component_col = f"{category}_fit_delta"
            out[component_col] = out[add_col] - out[drop_col]
            fit_components.append(component_col)

    if fit_components:
        out["category_fit_score"] = out[fit_components].sum(axis=1)
    else:
        out["category_fit_score"] = 0.0

    out["combined_add_drop_score"] = out["value_delta"] + out["category_fit_score"]

    return out.sort_values("combined_add_drop_score", ascending=False).reset_index(drop=True)