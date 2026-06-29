import pandas as pd

from nba_fantasy.snapshots import (
    roster_response_to_dataframe,
    free_agents_response_to_dataframe,
    save_snapshot_csv,
)


def test_roster_response_to_dataframe():
    response = {
        "success": True,
        "data": {
            "teamKey": "466.l.3706.t.9",
            "teamName": "Dame Time Management",
            "ownerName": "Graham",
            "players": [
                {
                    "playerKey": "466.p.6580",
                    "playerId": "6580",
                    "name": "Ayo Dosunmu",
                    "team": "MIN",
                    "position": "PG,SG,SF",
                    "selectedPosition": "PG",
                }
            ],
        },
    }

    df = roster_response_to_dataframe(response)

    assert len(df) == 1
    assert df.loc[0, "player"] == "Ayo Dosunmu"
    assert df.loc[0, "roster_slot"] == "PG"
    assert df.loc[0, "fantasy_team_name"] == "Dame Time Management"


def test_free_agents_response_to_dataframe():
    response = {
        "success": True,
        "data": {
            "leagueKey": "466.l.3706",
            "leagueName": "Lou Williams Memorial League",
            "freeAgents": [
                {
                    "playerKey": "466.p.6406",
                    "playerId": "6406",
                    "name": "Aaron Nesmith",
                    "team": "IND",
                    "position": "SG,SF",
                    "percentOwned": None,
                    "status": "GTD",
                }
            ],
        },
    }

    df = free_agents_response_to_dataframe(response)

    assert len(df) == 1
    assert df.loc[0, "player"] == "Aaron Nesmith"
    assert df.loc[0, "league_name"] == "Lou Williams Memorial League"
    assert df.loc[0, "status"] == "GTD"


def test_save_snapshot_csv(tmp_path):
    df = pd.DataFrame(
        {
            "player": ["A"],
            "team": ["AAA"],
        }
    )

    output_path = tmp_path / "snapshot.csv"

    saved_path = save_snapshot_csv(df, output_path)

    assert saved_path.exists()

    loaded = pd.read_csv(saved_path)

    assert loaded.loc[0, "player"] == "A"