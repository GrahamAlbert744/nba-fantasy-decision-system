"""
Data quality checks for NBA fantasy player datasets.

These functions validate that player projection/stat datasets contain the
columns required by the scoring model before rankings are calculated.
"""

from __future__ import annotations

import pandas as pd


REQUIRED_SCORING_COLUMNS = [
    "player",
    "pts",
    "reb",
    "ast",
    "stl",
    "blk",
    "threes",
    "fg_pct",
    "fga",
    "ft_pct",
    "fta",
    "to",
]

NUMERIC_SCORING_COLUMNS = [
    "pts",
    "reb",
    "ast",
    "stl",
    "blk",
    "threes",
    "fg_pct",
    "fga",
    "ft_pct",
    "fta",
    "to",
]


def get_missing_columns(df: pd.DataFrame, required_columns: list[str] | None = None) -> list[str]:
    """
    Return required columns that are missing from a dataframe.
    """
    if required_columns is None:
        required_columns = REQUIRED_SCORING_COLUMNS

    return [col for col in required_columns if col not in df.columns]


def validate_required_columns(
    df: pd.DataFrame,
    required_columns: list[str] | None = None,
) -> None:
    """
    Raise a ValueError if required columns are missing.
    """
    missing_columns = get_missing_columns(df, required_columns)

    if missing_columns:
        missing = ", ".join(missing_columns)
        raise ValueError(f"Missing required columns: {missing}")


def validate_numeric_columns(
    df: pd.DataFrame,
    numeric_columns: list[str] | None = None,
) -> None:
    """
    Raise a TypeError if scoring columns are not numeric.
    """
    if numeric_columns is None:
        numeric_columns = NUMERIC_SCORING_COLUMNS

    invalid_columns = []

    for col in numeric_columns:
        if col in df.columns and not pd.api.types.is_numeric_dtype(df[col]):
            invalid_columns.append(col)

    if invalid_columns:
        invalid = ", ".join(invalid_columns)
        raise TypeError(f"Columns must be numeric: {invalid}")


def validate_no_missing_values(
    df: pd.DataFrame,
    required_columns: list[str] | None = None,
) -> None:
    """
    Raise a ValueError if required scoring columns contain missing values.
    """
    if required_columns is None:
        required_columns = REQUIRED_SCORING_COLUMNS

    columns_to_check = [col for col in required_columns if col in df.columns]
    missing_counts = df[columns_to_check].isna().sum()
    missing_counts = missing_counts[missing_counts > 0]

    if not missing_counts.empty:
        details = ", ".join(
            f"{col}: {count}" for col, count in missing_counts.items()
        )
        raise ValueError(f"Missing values found in required columns: {details}")


def validate_player_scoring_input(df: pd.DataFrame) -> None:
    """
    Run all validation checks needed before scoring players.
    """
    validate_required_columns(df)
    validate_numeric_columns(df)
    validate_no_missing_values(df)