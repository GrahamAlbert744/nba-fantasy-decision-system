"""
Snapshot helpers for Flaim/Yahoo fantasy data.

These helpers convert Flaim-style roster and free-agent responses into
local CSV-friendly dataframes. This lets the project move from manually
typed sample CSVs toward saved league snapshots.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


def roster_response_to_dataframe(response: dict) -> pd.DataFrame:
    """
    Convert a Flaim roster response into a dataframe.

    Expected response shape:
    {
        "success": true,
        "data": {
            "teamKey": "...",
            "teamName": "...",
            "ownerName": "...",
            "players": [...]
        }
    }
    """
    data = response.get("data", {})
    players = data.get("players", [])

    rows = []

    for player in players:
        rows.append(
            {
                "player_key": player.get("playerKey"),
                "player_id": player.get("playerId"),
                "player": player.get("name"),
                "team": player.get("team"),
                "position": player.get("position"),
                "status": player.get("status", ""),
                "roster_slot": player.get("selectedPosition", ""),
                "fantasy_team_key": data.get("teamKey"),
                "fantasy_team_name": data.get("teamName"),
                "owner_name": data.get("ownerName"),
            }
        )

    return pd.DataFrame(rows)


def free_agents_response_to_dataframe(response: dict) -> pd.DataFrame:
    """
    Convert a Flaim free-agent response into a dataframe.

    Expected response shape:
    {
        "success": true,
        "data": {
            "leagueKey": "...",
            "leagueName": "...",
            "freeAgents": [...]
        }
    }
    """
    data = response.get("data", {})
    players = data.get("freeAgents", [])

    rows = []

    for player in players:
        rows.append(
            {
                "player_key": player.get("playerKey"),
                "player_id": player.get("playerId"),
                "player": player.get("name"),
                "team": player.get("team"),
                "position": player.get("position"),
                "status": player.get("status", ""),
                "percent_owned": player.get("percentOwned"),
                "league_key": data.get("leagueKey"),
                "league_name": data.get("leagueName"),
            }
        )

    return pd.DataFrame(rows)


def save_snapshot_csv(df: pd.DataFrame, output_path: str | Path) -> Path:
    """
    Save a snapshot dataframe as CSV.
    """
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    return output_path