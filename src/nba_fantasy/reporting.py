"""
Reporting helpers for NBA fantasy decision outputs.

These functions convert scored waiver/add-drop dataframes into readable
markdown reports that can be saved in data/outputs/.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


CATEGORY_LABELS = {
    "pts_z": "Points",
    "reb_z": "Rebounds",
    "ast_z": "Assists",
    "stl_z": "Steals",
    "blk_z": "Blocks",
    "threes_z": "Three-pointers",
    "fg_impact_z": "FG% impact",
    "ft_impact_z": "FT% impact",
    "to_z": "Turnovers",
}


def format_category_name(category: str) -> str:
    """
    Convert internal category z-score column names to readable labels.
    """
    return CATEGORY_LABELS.get(category, category)


def dataframe_to_markdown_table(
    df: pd.DataFrame,
    columns: list[str],
    round_digits: int = 2,
    max_rows: int = 10,
) -> str:
    """
    Convert selected dataframe columns to a markdown table.
    """
    available_columns = [col for col in columns if col in df.columns]
    table = df[available_columns].head(max_rows).copy()

    numeric_cols = table.select_dtypes(include="number").columns
    table[numeric_cols] = table[numeric_cols].round(round_digits)

    return table.to_markdown(index=False)


def build_waiver_report(
    team_profile: pd.Series,
    weak_categories: list[str],
    drop_candidates: pd.DataFrame,
    recommendations: pd.DataFrame,
    title: str = "Sample Waiver-Wire Report",
) -> str:
    """
    Build a human-readable markdown waiver report.
    """
    weak_category_labels = [
        format_category_name(category) for category in weak_categories
    ]

    team_profile_df = (
        team_profile.rename("team_total_z")
        .reset_index()
        .rename(columns={"index": "category"})
    )
    team_profile_df["category"] = team_profile_df["category"].apply(
        format_category_name
    )

    report_sections = []

    report_sections.append(f"# {title}")
    report_sections.append("")
    report_sections.append("## Purpose")
    report_sections.append("")
    report_sections.append(
        "This report summarizes sample waiver-wire add/drop recommendations "
        "using projected 9-category value and category-fit scoring."
    )
    report_sections.append("")
    report_sections.append(
        "This is still a proof-of-concept report based on sample projection data. "
        "It should not yet be treated as live fantasy advice."
    )

    report_sections.append("")
    report_sections.append("## Weak categories")
    report_sections.append("")
    report_sections.append(
        "The current model identifies these as the weakest roster categories:"
    )
    report_sections.append("")
    for category in weak_category_labels:
        report_sections.append(f"- {category}")

    report_sections.append("")
    report_sections.append("## Team category profile")
    report_sections.append("")
    report_sections.append(
        dataframe_to_markdown_table(
            team_profile_df,
            columns=["category", "team_total_z"],
            max_rows=20,
        )
    )

    report_sections.append("")
    report_sections.append("## Drop candidates")
    report_sections.append("")
    report_sections.append(
        dataframe_to_markdown_table(
            drop_candidates,
            columns=[
                "player",
                "team",
                "position",
                "status",
                "roster_slot",
                "total_9cat_z",
            ],
            max_rows=10,
        )
    )

    report_sections.append("")
    report_sections.append("## Top add/drop recommendations")
    report_sections.append("")
    report_sections.append(
        dataframe_to_markdown_table(
            recommendations,
            columns=[
                "player_add",
                "player_drop",
                "value_delta",
                "category_fit_score",
                "combined_add_drop_score",
            ],
            max_rows=10,
        )
    )

    report_sections.append("")
    report_sections.append("## Interpretation notes")
    report_sections.append("")
    report_sections.append(
        "- `value_delta` compares the free agent's projected total 9-category value "
        "against the drop candidate."
    )
    report_sections.append(
        "- `category_fit_score` measures whether the free agent improves the roster's "
        "weak categories."
    )
    report_sections.append(
        "- `combined_add_drop_score` is the current decision score: "
        "`value_delta + category_fit_score`."
    )
    report_sections.append(
        "- Positive scores suggest a potentially useful add/drop pairing."
    )
    report_sections.append(
        "- This model does not yet include schedule volume, matchup context, waiver "
        "rules, acquisition limits, or real injury severity."
    )

    return "\n".join(report_sections)


def save_markdown_report(report: str, output_path: str | Path) -> Path:
    """
    Save markdown report text to disk.
    """
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(report, encoding="utf-8")
    return output_path