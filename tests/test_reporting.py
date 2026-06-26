import pandas as pd

from nba_fantasy.reporting import (
    format_category_name,
    build_waiver_report,
)


def test_format_category_name():
    assert format_category_name("reb_z") == "Rebounds"
    assert format_category_name("unknown") == "unknown"


def test_build_waiver_report_contains_key_sections():
    team_profile = pd.Series(
        {
            "reb_z": -2.0,
            "blk_z": -1.5,
            "pts_z": 1.0,
        }
    )

    weak_categories = ["reb_z", "blk_z"]

    drop_candidates = pd.DataFrame(
        {
            "player": ["Weak Player"],
            "team": ["AAA"],
            "position": ["SG"],
            "status": [""],
            "roster_slot": ["BN"],
            "total_9cat_z": [-1.0],
        }
    )

    recommendations = pd.DataFrame(
        {
            "player_add": ["Good Add"],
            "player_drop": ["Weak Player"],
            "value_delta": [2.0],
            "category_fit_score": [1.0],
            "combined_add_drop_score": [3.0],
        }
    )

    report = build_waiver_report(
        team_profile=team_profile,
        weak_categories=weak_categories,
        drop_candidates=drop_candidates,
        recommendations=recommendations,
    )

    assert "# Sample Waiver-Wire Report" in report
    assert "## Weak categories" in report
    assert "## Drop candidates" in report
    assert "## Top add/drop recommendations" in report
    assert "Good Add" in report