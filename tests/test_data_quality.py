import pytest

import pandas as pd
import pytest

from nba_fantasy.scoring import add_9cat_scores

from nba_fantasy.data_quality import (
    get_missing_columns,
    validate_player_scoring_input,
    validate_required_columns,
    validate_numeric_columns,
    validate_no_missing_values,
)


def valid_player_df():
    return pd.DataFrame(
        {
            "player": ["A", "B", "C"],
            "pts": [20, 10, 5],
            "reb": [5, 10, 3],
            "ast": [6, 2, 1],
            "stl": [1.5, 0.5, 0.2],
            "blk": [0.5, 1.5, 0.1],
            "threes": [2, 1, 0],
            "fg_pct": [0.48, 0.55, 0.42],
            "fga": [15, 10, 8],
            "ft_pct": [0.85, 0.70, 0.90],
            "fta": [5, 3, 2],
            "to": [3, 2, 1],
        }
    )


def test_get_missing_columns_returns_missing_fields():
    df = valid_player_df().drop(columns=["pts", "reb"])

    missing = get_missing_columns(df)

    assert "pts" in missing
    assert "reb" in missing


def test_validate_required_columns_raises_for_missing_columns():
    df = valid_player_df().drop(columns=["pts"])

    with pytest.raises(ValueError, match="Missing required columns"):
        validate_required_columns(df)


def test_validate_numeric_columns_raises_for_non_numeric_columns():
    df = valid_player_df()
    df["pts"] = ["high", "medium", "low"]

    with pytest.raises(TypeError, match="Columns must be numeric"):
        validate_numeric_columns(df)


def test_validate_no_missing_values_raises_for_missing_values():
    df = valid_player_df()
    df.loc[0, "pts"] = None

    with pytest.raises(ValueError, match="Missing values found"):
        validate_no_missing_values(df)


def test_validate_player_scoring_input_accepts_valid_data():
    df = valid_player_df()

    validate_player_scoring_input(df)


def test_scoring_fails_with_missing_required_columns():
    df = pd.DataFrame(
        {
            "player": ["A", "B"],
            "pts": [10, 20],
        }
    )

    with pytest.raises(ValueError, match="Missing required columns"):
        add_9cat_scores(df)