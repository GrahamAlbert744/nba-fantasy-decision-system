import pandas as pd

from nba_fantasy.recommendations import (
    classify_recommendation,
    classify_confidence,
    add_recommendation_labels,
)


def test_classify_recommendation():
    assert classify_recommendation(6.0) == "Strong add"
    assert classify_recommendation(3.0) == "Moderate add"
    assert classify_recommendation(0.5) == "Marginal add"
    assert classify_recommendation(-1.0) == "Avoid"


def test_classify_confidence_high_without_injury():
    row = pd.Series(
        {
            "combined_add_drop_score": 6.0,
            "status_add": "",
            "status_drop": "",
        }
    )

    assert classify_confidence(row) == "High"


def test_classify_confidence_low_with_injured_add():
    row = pd.Series(
        {
            "combined_add_drop_score": 6.0,
            "status_add": "GTD",
            "status_drop": "",
        }
    )

    assert classify_confidence(row) == "Low"


def test_add_recommendation_labels():
    recommendations = pd.DataFrame(
        {
            "player_add": ["Good Add", "Bad Add"],
            "player_drop": ["Weak Drop", "Okay Drop"],
            "status_add": ["", "GTD"],
            "status_drop": ["", ""],
            "value_delta": [3.0, -1.0],
            "category_fit_score": [3.0, 0.0],
            "combined_add_drop_score": [6.0, -1.0],
        }
    )

    labeled = add_recommendation_labels(recommendations)

    assert "recommendation_tier" in labeled.columns
    assert "confidence" in labeled.columns
    assert labeled.iloc[0]["recommendation_tier"] == "Strong add"