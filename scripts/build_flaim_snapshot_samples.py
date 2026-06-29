from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
sys.path.insert(0, str(SRC_DIR))

from nba_fantasy.snapshots import (
    roster_response_to_dataframe,
    free_agents_response_to_dataframe,
    save_snapshot_csv,
)


ROSTER_RESPONSE = {
    "success": True,
    "data": {
        "teamKey": "466.l.3706.t.9",
        "teamName": "Dame Time Management",
        "ownerName": "Graham",
        "week": "current",
        "players": [
            {"playerKey": "466.p.6580", "playerId": "6580", "name": "Ayo Dosunmu", "team": "MIN", "position": "PG,SG,SF", "selectedPosition": "PG"},
            {"playerKey": "466.p.6032", "playerId": "6032", "name": "Grayson Allen", "team": "CHA", "position": "PG,SG,SF", "selectedPosition": "SG"},
            {"playerKey": "466.p.6696", "playerId": "6696", "name": "Bennedict Mathurin", "team": "LAC", "position": "SG,SF", "selectedPosition": "G"},
            {"playerKey": "466.p.6403", "playerId": "6403", "name": "Devin Vassell", "team": "SAS", "position": "SG,SF", "selectedPosition": "SF"},
            {"playerKey": "466.p.4614", "playerId": "4614", "name": "DeMar DeRozan", "team": "SAC", "position": "SF,PF", "selectedPosition": "PF", "status": "GTD"},
            {"playerKey": "466.p.10104", "playerId": "10104", "name": "Brandon Miller", "team": "CHA", "position": "SF,PF", "selectedPosition": "F", "status": "GTD"},
            {"playerKey": "466.p.5471", "playerId": "5471", "name": "Myles Turner", "team": "MIL", "position": "C", "selectedPosition": "C", "status": "GTD"},
            {"playerKey": "466.p.6253", "playerId": "6253", "name": "Naz Reid", "team": "CHA", "position": "PF,C", "selectedPosition": "C"},
            {"playerKey": "466.p.6754", "playerId": "6754", "name": "Julian Champagnie", "team": "SAS", "position": "SG,SF", "selectedPosition": "Util"},
            {"playerKey": "466.p.6702", "playerId": "6702", "name": "Jalen Williams", "team": "OKC", "position": "SF,PF", "selectedPosition": "Util", "status": "GTD"},
            {"playerKey": "466.p.6169", "playerId": "6169", "name": "Coby White", "team": "CHA", "position": "PG,SG", "selectedPosition": "BN"},
            {"playerKey": "466.p.5769", "playerId": "5769", "name": "Lauri Markkanen", "team": "UTA", "position": "SF,PF", "selectedPosition": "BN", "status": "GTD"},
            {"playerKey": "466.p.10095", "playerId": "10095", "name": "Anthony Black", "team": "ORL", "position": "PG,SG,SF", "selectedPosition": "BN"},
            {"playerKey": "466.p.6035", "playerId": "6035", "name": "Anfernee Simons", "team": "CHI", "position": "PG,SG", "selectedPosition": "IL", "status": "GTD"},
            {"playerKey": "466.p.5663", "playerId": "5663", "name": "Ivica Zubac", "team": "IND", "position": "C", "selectedPosition": "IL", "status": "GTD"},
        ],
    },
}


FREE_AGENTS_RESPONSE = {
    "success": True,
    "data": {
        "leagueKey": "466.l.3706",
        "leagueName": "Lou Williams Memorial League",
        "position": "ALL",
        "count": 25,
        "freeAgents": [
            {"playerKey": "466.p.6406", "playerId": "6406", "name": "Aaron Nesmith", "team": "IND", "position": "SG,SF", "percentOwned": None, "status": "GTD"},
            {"playerKey": "466.p.5482", "playerId": "5482", "name": "Bobby Portis", "team": "MIA", "position": "PF,C", "percentOwned": None},
            {"playerKey": "466.p.6711", "playerId": "6711", "name": "Christian Braun", "team": "DEN", "position": "SG,SF,PF", "percentOwned": None},
            {"playerKey": "466.p.10443", "playerId": "10443", "name": "Collin Murray-Boyles", "team": "TOR", "position": "PF,C", "percentOwned": None},
            {"playerKey": "466.p.6571", "playerId": "6571", "name": "Day'Ron Sharpe", "team": "BKN", "position": "C", "percentOwned": None, "status": "GTD"},
            {"playerKey": "466.p.6057", "playerId": "6057", "name": "De'Anthony Melton", "team": "GSW", "position": "PG,SG", "percentOwned": None},
            {"playerKey": "466.p.5660", "playerId": "5660", "name": "Dejounte Murray", "team": "NOP", "position": "PG,SG", "percentOwned": None, "status": "GTD"},
            {"playerKey": "466.p.10444", "playerId": "10444", "name": "Derik Queen", "team": "NOP", "position": "PF,C", "percentOwned": None},
            {"playerKey": "466.p.10070", "playerId": "10070", "name": "GG Jackson", "team": "MEM", "position": "SF,PF,C", "percentOwned": None, "status": "GTD"},
            {"playerKey": "466.p.6420", "playerId": "6420", "name": "Jaden McDaniels", "team": "MIN", "position": "SF,PF", "percentOwned": None},
            {"playerKey": "466.p.6402", "playerId": "6402", "name": "Jalen Smith", "team": "CHI", "position": "PF,C", "percentOwned": None, "status": "GTD"},
            {"playerKey": "466.p.10440", "playerId": "10440", "name": "Jeremiah Fears", "team": "NOP", "position": "PG,SG", "percentOwned": None},
            {"playerKey": "466.p.6549", "playerId": "6549", "name": "Jonathan Kuminga", "team": "ATL", "position": "SF,PF", "percentOwned": None},
            {"playerKey": "466.p.10272", "playerId": "10272", "name": "Kyshawn George", "team": "WAS", "position": "SG,SF,PF", "percentOwned": None, "status": "GTD"},
            {"playerKey": "466.p.5824", "playerId": "5824", "name": "Malik Monk", "team": "SAC", "position": "PG,SG", "percentOwned": None, "status": "GTD"},
            {"playerKey": "466.p.6725", "playerId": "6725", "name": "Max Christie", "team": "DAL", "position": "SG,SF", "percentOwned": None},
            {"playerKey": "466.p.6025", "playerId": "6025", "name": "Michael Porter Jr.", "team": "BKN", "position": "SF,PF", "percentOwned": None, "status": "GTD"},
            {"playerKey": "466.p.6219", "playerId": "6219", "name": "Nic Claxton", "team": "CHI", "position": "C", "percentOwned": None, "status": "GTD"},
            {"playerKey": "466.p.10469", "playerId": "10469", "name": "Nique Clifford", "team": "SAC", "position": "SG,SF", "percentOwned": None},
            {"playerKey": "466.p.6174", "playerId": "6174", "name": "P.J. Washington", "team": "DAL", "position": "SF,PF,C", "percentOwned": None, "status": "GTD"},
            {"playerKey": "466.p.6720", "playerId": "6720", "name": "Peyton Watson", "team": "DEN", "position": "SF,PF", "percentOwned": None, "status": "GTD"},
            {"playerKey": "466.p.4390", "playerId": "4390", "name": "Russell Westbrook", "team": "SAC", "position": "PG,SG", "percentOwned": None, "status": "GTD"},
            {"playerKey": "466.p.10048", "playerId": "10048", "name": "Scoot Henderson", "team": "POR", "position": "PG", "percentOwned": None},
            {"playerKey": "466.p.6697", "playerId": "6697", "name": "Shaedon Sharpe", "team": "POR", "position": "PG,SG,SF", "percentOwned": None},
            {"playerKey": "466.p.10065", "playerId": "10065", "name": "Toumani Camara", "team": "POR", "position": "SF,PF,C", "percentOwned": None},
        ],
    },
}


def main() -> None:
    output_dir = PROJECT_ROOT / "data" / "league_snapshots"
    output_dir.mkdir(parents=True, exist_ok=True)

    roster_df = roster_response_to_dataframe(ROSTER_RESPONSE)
    free_agents_df = free_agents_response_to_dataframe(FREE_AGENTS_RESPONSE)

    roster_path = save_snapshot_csv(
        roster_df,
        output_dir / "flaim_roster_snapshot_sample.csv",
    )

    free_agents_path = save_snapshot_csv(
        free_agents_df,
        output_dir / "flaim_free_agents_snapshot_sample.csv",
    )

    print(f"\nSaved roster snapshot to: {roster_path}")
    print(f"Saved free-agent snapshot to: {free_agents_path}")

    print("\nRoster snapshot preview:")
    print(roster_df[["player", "team", "position", "status", "roster_slot"]].head())

    print("\nFree-agent snapshot preview:")
    print(free_agents_df[["player", "team", "position", "status", "percent_owned"]].head())


if __name__ == "__main__":
    main()