from datetime import datetime
from pathlib import Path
import hashlib
import json
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


def calculate_file_sha256(path: Path) -> str | None:
    """
    Calculate the SHA-256 hash of a file.

    Returns None if the file does not exist.
    """
    path = Path(path)

    if not path.exists():
        return None

    sha256 = hashlib.sha256()

    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(8192), b""):
            sha256.update(chunk)

    return sha256.hexdigest()


def file_record(path: Path) -> dict:
    """
    Return file path, existence, size, and SHA-256 hash metadata.
    """
    path = Path(path)

    return {
        "path": str(path),
        "exists": path.exists(),
        "size_bytes": path.stat().st_size if path.exists() else None,
        "sha256": calculate_file_sha256(path),
    }


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


def save_run_manifest(
    manifest_path: Path,
    run_date: str,
    raw_roster_path: Path,
    raw_free_agents_path: Path,
    free_agent_path: Path,
    free_agent_projection_path: Path,
    roster_path: Path,
    roster_projection_path: Path,
    report_path: Path,
    latest_report_path: Path,
    punt_strategy: str,
    weak_category_count: int,
    drop_candidate_count: int,
    top_add_count: int,
) -> Path:
    """
    Save a JSON manifest describing one waiver-analysis run.

    The manifest records raw connector inputs, transformed snapshot inputs,
    projection files, output reports, model parameters, file sizes, and hashes.
    """
    manifest = {
        "run_date": run_date,
        "workflow": "waiver_analysis",
        "raw_inputs": {
            "raw_roster_json": file_record(raw_roster_path),
            "raw_free_agents_json": file_record(raw_free_agents_path),
        },
        "transformed_inputs": {
            "free_agent_snapshot": file_record(free_agent_path),
            "roster_snapshot": file_record(roster_path),
        },
        "projection_inputs": {
            "free_agent_projection_file": file_record(free_agent_projection_path),
            "roster_projection_file": file_record(roster_projection_path),
        },
        "outputs": {
            "dated_report": file_record(report_path),
            "latest_report": file_record(latest_report_path),
        },
        "parameters": {
            "punt_strategy": punt_strategy,
            "weak_category_count": weak_category_count,
            "drop_candidate_count": drop_candidate_count,
            "top_add_count": top_add_count,
        },
        "known_limitations": [
            "Uses Flaim-style sample raw JSON files.",
            "Uses Flaim-style sample snapshot CSVs.",
            "Uses manually created sample projection files.",
            "Does not yet include live matchup context.",
            "Does not yet include schedule volume.",
            "Does not yet include transaction limits or waiver priority.",
            "Does not yet include real injury severity.",
            "Does not yet record Git commit hash.",
            "Does not yet record Python or package versions.",
        ],
    }

    manifest_path.parent.mkdir(parents=True, exist_ok=True)

    manifest_path.write_text(
        json.dumps(manifest, indent=2),
        encoding="utf-8",
    )

    return manifest_path


def main() -> None:
    raw_dir = PROJECT_ROOT / "data" / "raw"
    snapshot_dir = PROJECT_ROOT / "data" / "league_snapshots"
    interim_dir = PROJECT_ROOT / "data" / "interim"
    output_dir = PROJECT_ROOT / "data" / "outputs"
    manifest_dir = PROJECT_ROOT / "data" / "run_manifests"

    output_dir.mkdir(parents=True, exist_ok=True)
    manifest_dir.mkdir(parents=True, exist_ok=True)

    date_stamp = get_date_stamp()

    raw_roster_path = raw_dir / "flaim_roster_raw_latest.json"
    raw_free_agents_path = raw_dir / "flaim_free_agents_raw_latest.json"

    free_agent_path = snapshot_dir / "flaim_free_agents_snapshot_sample.csv"
    free_agent_projection_path = interim_dir / "sample_player_projections.csv"
    roster_path = snapshot_dir / "flaim_roster_snapshot_sample.csv"
    roster_projection_path = interim_dir / "sample_roster_projections.csv"

    punt_strategy = "balanced"
    weak_category_count = 3
    drop_candidate_count = 5
    top_add_count = 5

    dated_output_path = output_dir / f"waiver_wire_report_{date_stamp}.md"
    latest_output_path = output_dir / "waiver_wire_report.md"
    manifest_path = manifest_dir / f"waiver_run_manifest_{date_stamp}.json"

    saved_report_path = run_waiver_analysis(
        free_agent_path=free_agent_path,
        free_agent_projection_path=free_agent_projection_path,
        roster_path=roster_path,
        roster_projection_path=roster_projection_path,
        output_path=dated_output_path,
        punt_strategy=punt_strategy,
        weak_category_count=weak_category_count,
        drop_candidate_count=drop_candidate_count,
        top_add_count=top_add_count,
    )

    latest_report_path = save_latest_copy(
        source_path=saved_report_path,
        latest_path=latest_output_path,
    )

    saved_manifest_path = save_run_manifest(
        manifest_path=manifest_path,
        run_date=date_stamp,
        raw_roster_path=raw_roster_path,
        raw_free_agents_path=raw_free_agents_path,
        free_agent_path=free_agent_path,
        free_agent_projection_path=free_agent_projection_path,
        roster_path=roster_path,
        roster_projection_path=roster_projection_path,
        report_path=saved_report_path,
        latest_report_path=latest_report_path,
        punt_strategy=punt_strategy,
        weak_category_count=weak_category_count,
        drop_candidate_count=drop_candidate_count,
        top_add_count=top_add_count,
    )

    print(f"\nSaved dated waiver-wire report to: {saved_report_path}")
    print(f"Saved latest waiver-wire report to: {latest_report_path}")
    print(f"Saved waiver run manifest to: {saved_manifest_path}")


if __name__ == "__main__":
    main()