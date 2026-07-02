from datetime import datetime, timezone
from pathlib import Path
import hashlib
import json
import platform
import shutil
import subprocess
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
    return datetime.now().strftime("%Y_%m_%d")


def get_created_at_timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def calculate_file_sha256(path: Path) -> str | None:
    path = Path(path)

    if not path.exists():
        return None

    sha256 = hashlib.sha256()

    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(8192), b""):
            sha256.update(chunk)

    return sha256.hexdigest()


def file_record(path: Path) -> dict:
    path = Path(path)

    return {
        "path": str(path),
        "exists": path.exists(),
        "size_bytes": path.stat().st_size if path.exists() else None,
        "sha256": calculate_file_sha256(path),
    }


def run_git_command(
    args: list[str],
    project_root: Path = PROJECT_ROOT,
) -> str | None:
    try:
        completed = subprocess.run(
            ["git", *args],
            cwd=project_root,
            capture_output=True,
            text=True,
            check=True,
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None

    output = completed.stdout.strip()
    return output if output else None


def run_command_capture(
    command: list[str],
    project_root: Path = PROJECT_ROOT,
) -> tuple[bool, str]:
    """
    Run a command and return success plus captured stdout/stderr.

    This is used for environment exports. It intentionally does not crash
    the waiver workflow if conda is unavailable.
    """
    try:
        completed = subprocess.run(
            command,
            cwd=project_root,
            capture_output=True,
            text=True,
            check=False,
        )
    except FileNotFoundError as error:
        return False, f"COMMAND_NOT_FOUND: {error}"

    output_parts = []

    if completed.stdout:
        output_parts.append(completed.stdout.strip())

    if completed.stderr:
        output_parts.append("\nSTDERR:\n" + completed.stderr.strip())

    output = "\n".join(output_parts).strip()

    if not output:
        output = f"Command exited with return code {completed.returncode}."

    return completed.returncode == 0, output


def save_text_file(
    path: Path,
    text: str,
) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def save_package_environment_exports(
    output_dir: Path,
    date_stamp: str,
    project_root: Path = PROJECT_ROOT,
) -> dict:
    """
    Save pip freeze and conda environment exports for reproducibility.

    If conda export fails, the failure output is still saved so the manifest
    records what happened.
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    pip_freeze_path = output_dir / f"pip_freeze_{date_stamp}.txt"
    conda_env_path = output_dir / f"conda_env_{date_stamp}.yml"

    pip_success, pip_output = run_command_capture(
        [sys.executable, "-m", "pip", "freeze"],
        project_root=project_root,
    )

    conda_success, conda_output = run_command_capture(
        ["conda", "env", "export", "--no-builds"],
        project_root=project_root,
    )

    if not pip_success:
        pip_output = f"# pip freeze failed\n\n{pip_output}"

    if not conda_success:
        conda_output = f"# conda env export failed\n\n{conda_output}"

    save_text_file(pip_freeze_path, pip_output + "\n")
    save_text_file(conda_env_path, conda_output + "\n")

    return {
        "pip_freeze": pip_freeze_path,
        "conda_env_export": conda_env_path,
        "pip_freeze_success": pip_success,
        "conda_env_export_success": conda_success,
    }


def get_git_commit_hash(project_root: Path = PROJECT_ROOT) -> str | None:
    return run_git_command(["rev-parse", "HEAD"], project_root=project_root)


def get_git_branch(project_root: Path = PROJECT_ROOT) -> str | None:
    return run_git_command(
        ["rev-parse", "--abbrev-ref", "HEAD"],
        project_root=project_root,
    )


def get_git_is_dirty(project_root: Path = PROJECT_ROOT) -> bool | None:
    status_output = run_git_command(
        ["status", "--porcelain"],
        project_root=project_root,
    )

    if status_output is None:
        clean_check = run_git_command(
            ["rev-parse", "--is-inside-work-tree"],
            project_root=project_root,
        )
        if clean_check is None:
            return None
        return False

    return bool(status_output)


def get_environment_metadata(
    project_root: Path = PROJECT_ROOT,
    script_name: str = "scripts/run_waiver_analysis.py",
) -> dict:
    return {
        "created_at": get_created_at_timestamp(),
        "project_root": str(project_root),
        "script": script_name,
        "command": f"python {script_name}",
        "git_commit_hash": get_git_commit_hash(project_root=project_root),
        "git_branch": get_git_branch(project_root=project_root),
        "git_is_dirty": get_git_is_dirty(project_root=project_root),
        "python_version": sys.version,
        "python_executable": sys.executable,
        "pandas_version": pd.__version__,
        "platform": {
            "system": platform.system(),
            "release": platform.release(),
            "version": platform.version(),
            "machine": platform.machine(),
            "processor": platform.processor(),
            "python_implementation": platform.python_implementation(),
        },
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
    pip_freeze_path: Path,
    conda_env_path: Path,
    pip_freeze_success: bool,
    conda_env_export_success: bool,
    punt_strategy: str,
    weak_category_count: int,
    drop_candidate_count: int,
    top_add_count: int,
    environment_metadata: dict | None = None,
) -> Path:
    if environment_metadata is None:
        environment_metadata = get_environment_metadata()

    manifest = {
        "run_date": run_date,
        "workflow": "waiver_analysis",
        "environment": environment_metadata,
        "environment_exports": {
            "pip_freeze": file_record(pip_freeze_path),
            "conda_env_export": file_record(conda_env_path),
            "pip_freeze_success": pip_freeze_success,
            "conda_env_export_success": conda_env_export_success,
        },
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
            "Git dirty status may be true during active development before committing.",
            "Does not yet record Flaim connector request metadata.",
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

    environment_exports = save_package_environment_exports(
        output_dir=manifest_dir,
        date_stamp=date_stamp,
        project_root=PROJECT_ROOT,
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
        pip_freeze_path=environment_exports["pip_freeze"],
        conda_env_path=environment_exports["conda_env_export"],
        pip_freeze_success=environment_exports["pip_freeze_success"],
        conda_env_export_success=environment_exports["conda_env_export_success"],
        punt_strategy=punt_strategy,
        weak_category_count=weak_category_count,
        drop_candidate_count=drop_candidate_count,
        top_add_count=top_add_count,
    )

    print(f"\nSaved dated waiver-wire report to: {saved_report_path}")
    print(f"Saved latest waiver-wire report to: {latest_report_path}")
    print(f"Saved pip freeze export to: {environment_exports['pip_freeze']}")
    print(f"Saved conda env export to: {environment_exports['conda_env_export']}")
    print(f"Saved waiver run manifest to: {saved_manifest_path}")


if __name__ == "__main__":
    main()