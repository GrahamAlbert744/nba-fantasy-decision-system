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
- Category-level z-score retention for category-fit analysis
- Graceful handling of players missing projection data
"""

from __future__ import annotations

import pandas as pd

from nba_fantasy.scoring import add_9cat_scores


SCORING_COLUMNS = [
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

PROJECTION_COLUMNS = [
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

PLAYER_METADATA_COLUMNS = [
    "player",
    "team",
    "position",
    "status",
    "roster_slot",
    "player_key",
    "player_id",
    "percent_owned",
    "fantasy_team_key",
    "fantasy_team_name",
    "owner_name",
    "league_key",
    "league_name",
]


def normalize_player_name(name: str) -> str:
    """
    Normalize player names for joining across data sources.

    Examples
    --------
    "P.J. Washington" -> "pj washington"
    "De'Anthony Melton" -> "deanthony melton"
    """
    if pd.isna(name):
        return ""

    return (
        str(name)
        .lower()
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
        Copy of dataframe with `player_key_join` added.
    """
    out = df.copy()
    out["player_key_join"] = out[player_col].apply(normalize_player_name)
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
        status, roster_slot, player_id, player_key, and related fields.
    projections:
        DataFrame containing projected fantasy stat fields.

    Returns
    -------
    pd.DataFrame
        Player metadata joined to projections.
    """
    player_metadata = add_player_join_key(players)
    projected_stats = add_player_join_key(projections)

    projection_cols_to_drop = ["player"]

    projected_stats_for_join = projected_stats.drop(
        columns=[col for col in projection_cols_to_drop if col in projected_stats.columns]
    )

    joined = player_metadata.merge(
        projected_stats_for_join,
        on="player_key_join",
        how="left",
        suffixes=("", "_projection"),
    )

    return joined.drop(columns=["player_key_join"])


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


def get_players_missing_projection_data(
    joined_players: pd.DataFrame,
) -> pd.DataFrame:
    """
    Return players that are missing one or more required projection fields.

    This is useful for auditing snapshot/projection joins.
    """
    available_projection_columns = [
        col for col in PROJECTION_COLUMNS if col in joined_players.columns
    ]

    if not available_projection_columns:
        return joined_players.copy()

    missing_mask = joined_players[available_projection_columns].isna().any(axis=1)

    metadata_columns = [
        col for col in PLAYER_METADATA_COLUMNS if col in joined_players.columns
    ]

    return joined_players.loc[missing_mask, metadata_columns].reset_index(drop=True)


def filter_players_with_complete_projections(
    joined_players: pd.DataFrame,
) -> pd.DataFrame:
    """
    Keep only players with complete projection data.

    Flaim snapshots may contain more players than the current sample projection
    file. Those unmatched players should be skipped rather than scored with
    missing values.
    """
    missing_projection_columns = [
        col for col in PROJECTION_COLUMNS if col not in joined_players.columns
    ]

    if missing_projection_columns:
        missing = ", ".join(missing_projection_columns)
        raise ValueError(f"Missing projection columns after join: {missing}")

    scorable_players = joined_players.dropna(subset=PROJECTION_COLUMNS).copy()

    if scorable_players.empty:
        raise ValueError(
            "No players have complete projection data. "
            "Check that player names match between the player snapshot and projection file."
        )

    return scorable_players


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

    Notes
    -----
    Players without complete projection data are skipped. This allows the
    workflow to use larger Flaim snapshots even when the sample projection
    dataset only covers a subset of players.
    """
    joined = join_players_to_projections(players, projections)
    scorable_players = filter_players_with_complete_projections(joined)

    players_to_score = scorable_players[SCORING_COLUMNS].copy()

    scored = add_9cat_scores(
        players_to_score,
        punt_strategy=punt_strategy,
    )

    metadata_columns = [
        col for col in PLAYER_METADATA_COLUMNS if col in scorable_players.columns
    ]

    metadata = scorable_players[metadata_columns].copy()

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
        "player_key_add",
        "player_id_add",
        "percent_owned_add",
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
        "player_key_drop",
        "player_id_drop",
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