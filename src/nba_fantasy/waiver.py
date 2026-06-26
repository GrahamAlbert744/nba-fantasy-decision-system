"""
Waiver-wire analysis helpers.

This module joins league availability data from Flaim/Yahoo with projected
player stats, then ranks available players using the 9-category scoring model.
"""

from __future__ import annotations

import pandas as pd

from nba_fantasy.scoring import add_9cat_scores


def normalize_player_name(name: str) -> str:
    """
    Normalize player names for joining across data sources.
    """
    return (
        name.lower()
        .replace(".", "")
        .replace("'", "")
        .replace("-", " ")
        .strip()
    )


def add_player_join_key(df: pd.DataFrame, player_col: str = "player") -> pd.DataFrame:
    """
    Add a normalized player-name join key.
    """
    out = df.copy()
    out["player_key"] = out[player_col].apply(normalize_player_name)
    return out


def join_free_agents_to_projections(
    free_agents: pd.DataFrame,
    projections: pd.DataFrame,
) -> pd.DataFrame:
    """
    Join Flaim/Yahoo free-agent availability to player projections.
    """
    fa = add_player_join_key(free_agents)
    proj = add_player_join_key(projections)

    joined = fa.merge(
        proj.drop(columns=["player"]),
        on="player_key",
        how="left",
        suffixes=("", "_projection"),
    )

    return joined.drop(columns=["player_key"])


def rank_available_players(
    free_agents: pd.DataFrame,
    projections: pd.DataFrame,
    punt_strategy: str = "balanced",
) -> pd.DataFrame:
    """
    Rank available players using projected 9-category value.
    """
    joined = join_free_agents_to_projections(free_agents, projections)

    scoring_columns = [
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

    players_to_score = joined[scoring_columns].copy()
    scored = add_9cat_scores(players_to_score, punt_strategy=punt_strategy)

    metadata_columns = ["player", "team", "position", "status"]
    metadata = joined[metadata_columns].copy()

    ranked = metadata.merge(
        scored,
        on="player",
        how="left",
    )

    return ranked.sort_values("total_9cat_z", ascending=False).reset_index(drop=True)