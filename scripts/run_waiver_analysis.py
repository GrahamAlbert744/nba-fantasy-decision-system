from datetime import datetime
from pathlib import Path
import shutil
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


def get_date_stamp() -> str:
    """
    Return a YYYY_MM_DD date stamp for output filenames.
    """
    return datetime.now().strftime("%Y_%m_%d")


def run_waiver_analysis(
    free_agent_path: Path,
    free_agent_projection_path: Path,
    roster_path: Path,
    roster_projection_path: Path,
    output_path: Path,
    punt_strategy: str = "balanced",
    weak_category_count: int = 3,
    drop_candidate_count: int = 5,
    top_add_count: int = 5,
) -> Path:
    """
    Run the full waiver-wire analysis workflow.

    This workflow consumes Flaim-style roster/free-agent snapshot CSVs,
    joins them to projection CSVs, scores players, creates add/drop
    recommendations, and writes a markdown report.
    """
    free_agents = pd.read_csv(free_agent_path)
    free_agent_projections = pd.read_csv(free_agent_projection_path)

    roster = pd.read_csv(roster_path)
    roster_projections = pd.read_csv(roster_projection_path)

    ranked_free_agents = rank_available_players(
        free_agents=free_agents,
        projections=free_agent_projections,
        punt_strategy=punt_strategy,
    )

    ranked_roster = rank_rostered_players(
        roster=roster,
        projections=roster_projections,
        punt_strategy=punt_strategy,
    )

    team_profile = calculate_team_category_profile(ranked_roster)
    weak_categories = identify_weak_categories(
        team_profile,
        n=weak_category_count,
    )

    drop_candidates = identify_drop_candidates(
        ranked_roster=ranked_roster,
        n=drop_candidate_count,
    )

    base_recommendations = create_add_drop_recommendations(
        ranked_free_agents=ranked_free_agents,
        drop_candidates=drop_candidates,
        top_adds=top_add_count,
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
        title="Waiver-Wire Report",
    )

    saved_path = save_markdown_report(
        report=report,
        output_path=output_path,
    )

    return saved_path


def save_latest_copy(
    source_path: Path,
    latest_path: Path,
) -> Path:
    """
    Copy a dated report to a stable latest-report filename.
    """
    latest_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source_path, latest_path)
    return latest_path


def main() -> None:
    snapshot_dir = PROJECT_ROOT / "data" / "league_snapshots"
    interim_dir = PROJECT_ROOT / "data" / "interim"
    output_dir = PROJECT_ROOT / "data" / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)

    date_stamp = get_date_stamp()

    dated_output_path = output_dir / f"waiver_wire_report_{date_stamp}.md"
    latest_output_path = output_dir / "waiver_wire_report.md"

    saved_path = run_waiver_analysis(
        free_agent_path=snapshot_dir / "flaim_free_agents_snapshot_sample.csv",
        free_agent_projection_path=interim_dir / "sample_player_projections.csv",
        roster_path=snapshot_dir / "flaim_roster_snapshot_sample.csv",
        roster_projection_path=interim_dir / "sample_roster_projections.csv",
        output_path=dated_output_path,
        punt_strategy="balanced",
        weak_category_count=3,
        drop_candidate_count=5,
        top_add_count=5,
    )

    latest_path = save_latest_copy(
        source_path=saved_path,
        latest_path=latest_output_path,
    )

    print(f"\nSaved dated waiver-wire report to: {saved_path}")
    print(f"Saved latest waiver-wire report to: {latest_path}")


if __name__ == "__main__":
    main()