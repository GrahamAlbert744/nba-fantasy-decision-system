from pathlib import Path
import sys

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
sys.path.insert(0, str(SRC_DIR))

from nba_fantasy.scoring import add_9cat_scores


def build_sample_player_data() -> pd.DataFrame:
    """Create a small sample dataset to test 9-category scoring logic."""
    return pd.DataFrame(
        [
            {
                "player": "Nikola Jokic",
                "pts": 26.4,
                "reb": 12.4,
                "ast": 9.0,
                "stl": 1.4,
                "blk": 0.9,
                "threes": 1.1,
                "fg_pct": 0.583,
                "fga": 17.9,
                "ft_pct": 0.817,
                "fta": 5.5,
                "to": 3.0,
            },
            {
                "player": "Shai Gilgeous-Alexander",
                "pts": 30.1,
                "reb": 5.5,
                "ast": 6.2,
                "stl": 2.0,
                "blk": 0.9,
                "threes": 1.3,
                "fg_pct": 0.535,
                "fga": 20.0,
                "ft_pct": 0.875,
                "fta": 8.7,
                "to": 2.2,
            },
            {
                "player": "Anthony Davis",
                "pts": 24.7,
                "reb": 12.6,
                "ast": 3.5,
                "stl": 1.2,
                "blk": 2.3,
                "threes": 0.4,
                "fg_pct": 0.556,
                "fga": 17.2,
                "ft_pct": 0.816,
                "fta": 6.8,
                "to": 2.1,
            },
            {
                "player": "Stephen Curry",
                "pts": 26.4,
                "reb": 4.5,
                "ast": 5.1,
                "stl": 0.7,
                "blk": 0.4,
                "threes": 4.8,
                "fg_pct": 0.450,
                "fga": 19.5,
                "ft_pct": 0.923,
                "fta": 4.4,
                "to": 2.8,
            },
            {
                "player": "Myles Turner",
                "pts": 17.1,
                "reb": 6.9,
                "ast": 1.3,
                "stl": 0.5,
                "blk": 1.9,
                "threes": 1.5,
                "fg_pct": 0.524,
                "fga": 11.8,
                "ft_pct": 0.773,
                "fta": 3.6,
                "to": 1.4,
            },
            {
                "player": "DeMar DeRozan",
                "pts": 22.1,
                "reb": 4.3,
                "ast": 5.3,
                "stl": 1.1,
                "blk": 0.6,
                "threes": 0.9,
                "fg_pct": 0.480,
                "fga": 17.3,
                "ft_pct": 0.853,
                "fta": 6.5,
                "to": 1.7,
            },
            {
                "player": "Nic Claxton",
                "pts": 11.8,
                "reb": 9.9,
                "ast": 2.1,
                "stl": 0.7,
                "blk": 2.1,
                "threes": 0.0,
                "fg_pct": 0.629,
                "fga": 7.7,
                "ft_pct": 0.551,
                "fta": 2.9,
                "to": 1.3,
            },
            {
                "player": "Klay Thompson",
                "pts": 17.9,
                "reb": 3.3,
                "ast": 2.3,
                "stl": 0.6,
                "blk": 0.5,
                "threes": 3.5,
                "fg_pct": 0.432,
                "fga": 15.0,
                "ft_pct": 0.927,
                "fta": 1.0,
                "to": 1.5,
            },
        ]
    )


def main() -> None:
    output_dir = PROJECT_ROOT / "data" / "processed"
    output_dir.mkdir(parents=True, exist_ok=True)

    players = build_sample_player_data()

    balanced = add_9cat_scores(players)
    punt_ft = add_9cat_scores(players, punt_categories=["ft_impact"])
    punt_to = add_9cat_scores(players, punt_categories=["to"])

    balanced.to_csv(output_dir / "sample_player_rankings_balanced.csv", index=False)
    punt_ft.to_csv(output_dir / "sample_player_rankings_punt_ft.csv", index=False)
    punt_to.to_csv(output_dir / "sample_player_rankings_punt_to.csv", index=False)

    print("\nBalanced rankings:")
    print(balanced[["player", "total_9cat_z"]].round(2))

    print("\nPunt FT rankings:")
    print(punt_ft[["player", "total_9cat_z"]].round(2))

    print("\nPunt TO rankings:")
    print(punt_to[["player", "total_9cat_z"]].round(2))

    print("\nSaved sample rankings to data/processed/")


if __name__ == "__main__":
    main()