from pathlib import Path
import sys

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
sys.path.insert(0, str(SRC_DIR))

from nba_fantasy.reporting import build_waiver_report, save_markdown_report
from nba_fantasy.recommendations import add_recommendation_labels
from nba_fantasy.team_needs import (
    calculate_team_category_profile,
    identify_weak_categories,
    add_category_fit_score,
)
from nba_fantasy.waiver import (
    rank_available_players,
    rank_rostered_players,
    identify_drop_candidates,
    create_add_drop_recommendations,
)


def main() -> None:
    """
    Generate a sample waiver-wire report.

    This script runs the full sample waiver pipeline:

    1. Load sample Flaim free-agent data.
    2. Load sample free-agent projections.
    3. Load sample roster data.
    4. Load sample roster projections.
    5. Rank available players.
    6. Rank rostered players.
    7. Identify weak team categories.
    8. Identify drop candidates.
    9. Create add/drop recommendations.
    10. Add category-fit scores.
    11. Add recommendation tiers and confidence labels.
    12. Save a markdown waiver report to data/outputs/.
    """
    interim_dir = PROJECT_ROOT / "data" / "interim"
    output_dir = PROJECT_ROOT / "data" / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)

    free_agent_path = interim_dir / "flaim_free_agents_sample.csv"
    free_agent_projection_path = interim_dir / "sample_player_projections.csv"
    roster_path = interim_dir / "flaim_roster_sample.csv"
    roster_projection_path = interim_dir / "sample_roster_projections.csv"

    free_agents = pd.read_csv(free_agent_path)
    free_agent_projections = pd.read_csv(free_agent_projection_path)

    roster = pd.read_csv(roster_path)
    roster_projections = pd.read_csv(roster_projection_path)

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

    team_profile = calculate_team_category_profile(ranked_roster)
    weak_categories = identify_weak_categories(team_profile, n=3)

    drop_candidates = identify_drop_candidates(
        ranked_roster=ranked_roster,
        n=5,
    )

    base_recommendations = create_add_drop_recommendations(
        ranked_free_agents=ranked_free_agents,
        drop_candidates=drop_candidates,
        top_adds=5,
    )

    category_fit_recommendations = add_category_fit_score(
        recommendations=base_recommendations,
        weak_categories=weak_categories,
    )

    labeled_recommendations = add_recommendation_labels(
        category_fit_recommendations
    )

    report = build_waiver_report(
        team_profile=team_profile,
        weak_categories=weak_categories,
        drop_candidates=drop_candidates,
        recommendations=labeled_recommendations,
        title="Sample Waiver-Wire Report",
    )

    output_path = save_markdown_report(
        report=report,
        output_path=output_dir / "sample_waiver_report.md",
    )

    print(f"\nSaved waiver report to: {output_path}")

    print("\nWeak categories:")
    print(weak_categories)

    print("\nTop labeled recommendations:")
    print(
        labeled_recommendations[
            [
                "player_add",
                "player_drop",
                "recommendation_tier",
                "confidence",
                "value_delta",
                "category_fit_score",
                "combined_add_drop_score",
            ]
        ]
        .head(10)
        .round(2)
    )


if __name__ == "__main__":
    main()