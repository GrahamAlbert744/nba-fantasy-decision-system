from pathlib import Path
import sys

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
sys.path.insert(0, str(SRC_DIR))

from nba_fantasy.waiver import (
    rank_available_players,
    rank_rostered_players,
    identify_drop_candidates,
    create_add_drop_recommendations,
)


def main() -> None:
    interim_dir = PROJECT_ROOT / "data" / "interim"
    output_dir = PROJECT_ROOT / "data" / "processed"
    output_dir.mkdir(parents=True, exist_ok=True)

    free_agents = pd.read_csv(interim_dir / "flaim_free_agents_sample.csv")
    free_agent_projections = pd.read_csv(interim_dir / "sample_player_projections.csv")

    roster = pd.read_csv(interim_dir / "flaim_roster_sample.csv")
    roster_projections = pd.read_csv(interim_dir / "sample_roster_projections.csv")

    ranked_free_agents = rank_available_players(
        free_agents=free_agents,
        projections=free_agent_projections,
        punt_strategy="balanced",
    )

    ranked_roster = rank_rostered_players(
        roster=roster,
        projections=roster_projections,
        punt_strategy="balanced",
    )

    drop_candidates = identify_drop_candidates(
        ranked_roster=ranked_roster,
        n=5,
    )

    recommendations = create_add_drop_recommendations(
        ranked_free_agents=ranked_free_agents,
        drop_candidates=drop_candidates,
        top_adds=5,
    )

    ranked_free_agents.to_csv(output_dir / "sample_ranked_free_agents.csv", index=False)
    ranked_roster.to_csv(output_dir / "sample_ranked_roster.csv", index=False)
    drop_candidates.to_csv(output_dir / "sample_drop_candidates.csv", index=False)
    recommendations.to_csv(output_dir / "sample_add_drop_recommendations.csv", index=False)

    print("\nDrop candidates:")
    print(
        drop_candidates[
            ["player", "team", "position", "status", "roster_slot", "total_9cat_z"]
        ].round(2)
    )

    print("\nTop add/drop recommendations:")
    print(
        recommendations[
            [
                "player_add",
                "total_9cat_z_add",
                "player_drop",
                "total_9cat_z_drop",
                "value_delta",
            ]
        ]
        .head(10)
        .round(2)
    )

    print("\nSaved add/drop outputs to data/processed/")


if __name__ == "__main__":
    main()