"""
Waiver-wire analysis helpers.

This module joins league availability data from Flaim/Yahoo with projected
player stats, ranks available players, ranks rostered players, and creates
basic add/drop comparisons.

The module currently supports:
- Free-agent projection joins
- Roster projection joins
- Available-player rankings
- Rostered-player rankings
- Drop-candidate detection
- Add/drop value-delta recommendations
- Category-level z-score retention for later category-fit analysis
"""

from __future__ import annotations

import pandas as pd

from nba_fantasy.scoring import add_9cat_scores


def normalize_player_name(name: str) -> str:
    """
    Normalize player names for joining across data sources.

    Examples
    --------
    "P.J. Washington" -> "pj washington"
    "De'Anthony Melton" -> "deanthony melton"
    """
    return (
        name.lower()
        .replace(".", "")
        .replace("'", "")
        .replace("-", " ")
        .strip()
    )


def add_player_join_key(
    df: pd.DataFrame,
    player_col: str = "player",
) -> pd.DataFrame:
    """
    Add a normalized player-name join key.

    Parameters
    ----------
    df:
        Player dataframe.
    player_col:
        Name of the player-name column.

    Returns
    -------
    pd.DataFrame
        Copy of dataframe with `player_key` added.
    """
    out = df.copy()
    out["player_key"] = out[player_col].apply(normalize_player_name)
    return out


def join_players_to_projections(
    players: pd.DataFrame,
    projections: pd.DataFrame,
) -> pd.DataFrame:
    """
    Join player metadata to player projections.

    This generic function is used for both free agents and rostered players.

    Parameters
    ----------
    players:
        DataFrame containing player metadata such as player, team, position,
        status, and optionally roster_slot.
    projections:
        DataFrame containing projected fantasy stat fields.

    Returns
    -------
    pd.DataFrame
        Player metadata joined to projections.
    """
    player_metadata = add_player_join_key(players)
    projected_stats = add_player_join_key(projections)

    joined = player_metadata.merge(
        projected_stats.drop(columns=["player"]),
        on="player_key",
        how="left",
        suffixes=("", "_projection"),
    )

    return joined.drop(columns=["player_key"])


def join_free_agents_to_projections(
    free_agents: pd.DataFrame,
    projections: pd.DataFrame,
) -> pd.DataFrame:
    """
    Join Flaim/Yahoo free-agent availability to player projections.
    """
    return join_players_to_projections(
        players=free_agents,
        projections=projections,
    )


def rank_players_with_projections(
    players: pd.DataFrame,
    projections: pd.DataFrame,
    punt_strategy: str = "balanced",
) -> pd.DataFrame:
    """
    Rank any player list using projected 9-category value.

    Parameters
    ----------
    players:
        DataFrame containing player metadata.
    projections:
        DataFrame containing projected player stats.
    punt_strategy:
        Named punt strategy. Example: "balanced", "punt_ft", "punt_to".

    Returns
    -------
    pd.DataFrame
        Ranked players with metadata, projected stats, category z-scores,
        and total 9-category value.
    """
    joined = join_players_to_projections(players, projections)

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

    scored = add_9cat_scores(
        players_to_score,
        punt_strategy=punt_strategy,
    )

    metadata_columns = [
        col
        for col in ["player", "team", "position", "status", "roster_slot"]
        if col in joined.columns
    ]

    metadata = joined[metadata_columns].copy()

    ranked = metadata.merge(
        scored,
        on="player",
        how="left",
    )

    return ranked.sort_values(
        "total_9cat_z",
        ascending=False,
    ).reset_index(drop=True)


def rank_available_players(
    free_agents: pd.DataFrame,
    projections: pd.DataFrame,
    punt_strategy: str = "balanced",
) -> pd.DataFrame:
    """
    Rank available players using projected 9-category value.
    """
    return rank_players_with_projections(
        players=free_agents,
        projections=projections,
        punt_strategy=punt_strategy,
    )


def rank_rostered_players(
    roster: pd.DataFrame,
    projections: pd.DataFrame,
    punt_strategy: str = "balanced",
) -> pd.DataFrame:
    """
    Rank rostered players using projected 9-category value.
    """
    return rank_players_with_projections(
        players=roster,
        projections=projections,
        punt_strategy=punt_strategy,
    )


def identify_drop_candidates(
    ranked_roster: pd.DataFrame,
    exclude_slots: list[str] | None = None,
    n: int = 5,
) -> pd.DataFrame:
    """
    Identify the lowest-ranked rostered players as drop candidates.

    By default, IL players are excluded because dropping injured-list players
    may not create an active roster spot.

    Parameters
    ----------
    ranked_roster:
        Ranked roster dataframe.
    exclude_slots:
        Roster slots to exclude from drop-candidate logic.
    n:
        Number of drop candidates to return.

    Returns
    -------
    pd.DataFrame
        Lowest-ranked rostered players, excluding selected roster slots.
    """
    if exclude_slots is None:
        exclude_slots = ["IL"]

    out = ranked_roster.copy()

    if "roster_slot" in out.columns:
        out = out[~out["roster_slot"].isin(exclude_slots)]

    return (
        out.sort_values("total_9cat_z", ascending=True)
        .head(n)
        .reset_index(drop=True)
    )


def create_add_drop_recommendations(
    ranked_free_agents: pd.DataFrame,
    drop_candidates: pd.DataFrame,
    top_adds: int = 5,
) -> pd.DataFrame:
    """
    Create simple add/drop pairings.

    Each top free agent is compared against each drop candidate.

    Positive value_delta means the free agent projects better than the
    rostered drop candidate by total 9-category value.

    This function also retains category-level z-score columns so that
    later modules can calculate category-fit scores.
    """
    adds = ranked_free_agents.head(top_adds).copy()
    drops = drop_candidates.copy()

    recommendations = adds.merge(
        drops,
        how="cross",
        suffixes=("_add", "_drop"),
    )

    recommendations["value_delta"] = (
        recommendations["total_9cat_z_add"]
        - recommendations["total_9cat_z_drop"]
    )

    columns = [
        "player_add",
        "team_add",
        "position_add",
        "status_add",
        "total_9cat_z_add",
        "pts_z_add",
        "reb_z_add",
        "ast_z_add",
        "stl_z_add",
        "blk_z_add",
        "threes_z_add",
        "fg_impact_z_add",
        "ft_impact_z_add",
        "to_z_add",
        "player_drop",
        "team_drop",
        "position_drop",
        "status_drop",
        "roster_slot",
        "total_9cat_z_drop",
        "pts_z_drop",
        "reb_z_drop",
        "ast_z_drop",
        "stl_z_drop",
        "blk_z_drop",
        "threes_z_drop",
        "fg_impact_z_drop",
        "ft_impact_z_drop",
        "to_z_drop",
        "value_delta",
    ]

    available_columns = [
        col for col in columns if col in recommendations.columns
    ]

    return (
        recommendations[available_columns]
        .sort_values("value_delta", ascending=False)
        .reset_index(drop=True)
    )