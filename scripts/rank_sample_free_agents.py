from pathlib import Path
import sys

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
sys.path.insert(0, str(SRC_DIR))

from nba_fantasy.waiver import rank_available_players


def main() -> None:
    free_agent_path = PROJECT_ROOT / "data" / "interim" / "flaim_free_agents_sample.csv"
    projection_path = PROJECT_ROOT / "data" / "interim" / "sample_player_projections.csv"
    output_dir = PROJECT_ROOT / "data" / "processed"
    output_dir.mkdir(parents=True, exist_ok=True)

    free_agents = pd.read_csv(free_agent_path)
    projections = pd.read_csv(projection_path)

    ranked = rank_available_players(
        free_agents=free_agents,
        projections=projections,
        punt_strategy="balanced",
    )

    output_path = output_dir / "sample_free_agent_rankings.csv"
    ranked.to_csv(output_path, index=False)

    print("\nTop available players:")
    print(
        ranked[
            [
                "player",
                "team",
                "position",
                "status",
                "total_9cat_z",
                "pts",
                "reb",
                "ast",
                "stl",
                "blk",
                "threes",
            ]
        ]
        .head(10)
        .round(2)
    )

    print(f"\nSaved ranked free agents to: {output_path}")


if __name__ == "__main__":
    main()