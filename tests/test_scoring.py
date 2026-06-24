import pandas as pd

from src.nba_fantasy.scoring import add_basic_9cat_scores


def test_add_basic_9cat_scores_creates_total_score():
    df = pd.DataFrame({
        "player": ["A", "B", "C"],
        "pts": [20, 10, 5],
        "reb": [5, 10, 3],
        "ast": [6, 2, 1],
        "stl": [1.5, 0.5, 0.2],
        "blk": [0.5, 1.5, 0.1],
        "threes": [2, 1, 0],
        "fg_pct": [0.48, 0.55, 0.42],
        "ft_pct": [0.85, 0.70, 0.90],
        "to": [3, 2, 1],
    })

    scored = add_basic_9cat_scores(df)

    assert "total_9cat_z" in scored.columns
    assert len(scored) == 3
