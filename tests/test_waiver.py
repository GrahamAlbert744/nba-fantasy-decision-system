import pandas as pd

from nba_fantasy.waiver import (
    normalize_player_name,
    join_free_agents_to_projections,
    rank_available_players,
)


def test_normalize_player_name():
    assert normalize_player_name("P.J. Washington") == "pj washington"
    assert normalize_player_name("De'Anthony Melton") == "deanthony melton"


def test_join_free_agents_to_projections():
    free_agents = pd.DataFrame(
        {
            "player": ["P.J. Washington", "Nic Claxton"],
            "team": ["DAL", "CHI"],
            "position": ["SF,PF,C", "C"],
            "status": ["GTD", "GTD"],
        }
    )

    projections = pd.DataFrame(
        {
            "player": ["PJ Washington", "Nic Claxton"],
            "pts": [13.5, 11.8],
            "reb": [5.9, 9.9],
            "ast": [2.2, 2.1],
            "stl": [0.9, 0.7],
            "blk": [0.8, 2.1],
            "threes": [1.8, 0.0],
            "fg_pct": [0.455, 0.629],
            "fga": [10.8, 7.7],
            "ft_pct": [0.720, 0.551],
            "fta": [2.0, 2.9],
            "to": [1.4, 1.3],
        }
    )

    joined = join_free_agents_to_projections(free_agents, projections)

    assert "pts" in joined.columns
    assert joined["pts"].notna().all()


def test_rank_available_players_returns_scores():
    free_agents = pd.DataFrame(
        {
            "player": ["P.J. Washington", "Nic Claxton", "Bobby Portis"],
            "team": ["DAL", "CHI", "MIA"],
            "position": ["SF,PF,C", "C", "PF,C"],
            "status": ["GTD", "GTD", ""],
        }
    )

    projections = pd.DataFrame(
        {
            "player": ["PJ Washington", "Nic Claxton", "Bobby Portis"],
            "pts": [13.5, 11.8, 14.0],
            "reb": [5.9, 9.9, 8.1],
            "ast": [2.2, 2.1, 1.5],
            "stl": [0.9, 0.7, 0.7],
            "blk": [0.8, 2.1, 0.5],
            "threes": [1.8, 0.0, 1.2],
            "fg_pct": [0.455, 0.629, 0.500],
            "fga": [10.8, 7.7, 11.1],
            "ft_pct": [0.720, 0.551, 0.780],
            "fta": [2.0, 2.9, 2.1],
            "to": [1.4, 1.3, 1.2],
        }
    )

    ranked = rank_available_players(free_agents, projections)

    assert "total_9cat_z" in ranked.columns
    assert len(ranked) == 3