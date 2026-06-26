import pandas as pd

from nba_fantasy.team_needs import (
    calculate_team_category_profile,
    identify_weak_categories,
    add_category_fit_score,
)


def test_calculate_team_category_profile():
    ranked_roster = pd.DataFrame(
        {
            "player": ["A", "B"],
            "pts_z": [1.0, -0.5],
            "reb_z": [-1.0, -0.5],
            "ast_z": [0.5, 0.5],
            "stl_z": [0.2, 0.1],
            "blk_z": [-0.8, -0.2],
            "threes_z": [1.2, 0.3],
            "fg_impact_z": [-0.3, -0.2],
            "ft_impact_z": [0.1, 0.4],
            "to_z": [0.0, 0.2],
        }
    )

    profile = calculate_team_category_profile(ranked_roster)

    assert profile["reb_z"] == -1.5
    assert profile["ast_z"] == 1.0


def test_identify_weak_categories():
    team_profile = pd.Series(
        {
            "pts_z": 2.0,
            "reb_z": -3.0,
            "ast_z": 1.0,
            "blk_z": -2.0,
            "ft_impact_z": -1.0,
        }
    )

    weak = identify_weak_categories(team_profile, n=2)

    assert weak == ["reb_z", "blk_z"]


def test_add_category_fit_score():
    recommendations = pd.DataFrame(
        {
            "player_add": ["Good Fit", "Bad Fit"],
            "player_drop": ["Weak Drop", "Weak Drop"],
            "value_delta": [1.0, 2.0],
            "reb_z_add": [2.0, -1.0],
            "reb_z_drop": [-1.0, -1.0],
            "blk_z_add": [1.0, -2.0],
            "blk_z_drop": [0.0, 0.0],
        }
    )

    scored = add_category_fit_score(
        recommendations=recommendations,
        weak_categories=["reb_z", "blk_z"],
    )

    assert "category_fit_score" in scored.columns
    assert "combined_add_drop_score" in scored.columns
    assert scored.iloc[0]["player_add"] == "Good Fit"