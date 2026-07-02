import json
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.run_waiver_analysis import (
    calculate_file_sha256,
    file_record,
    get_environment_metadata,
    get_git_branch,
    get_git_commit_hash,
    get_git_is_dirty,
    run_waiver_analysis,
    save_latest_copy,
    save_package_environment_exports,
    save_run_manifest,
)


def test_run_waiver_analysis_creates_report_from_snapshot_csvs(tmp_path):
    snapshot_dir = PROJECT_ROOT / "data" / "league_snapshots"
    interim_dir = PROJECT_ROOT / "data" / "interim"

    output_path = tmp_path / "test_waiver_report.md"

    saved_path = run_waiver_analysis(
        free_agent_path=snapshot_dir / "flaim_free_agents_snapshot_sample.csv",
        free_agent_projection_path=interim_dir / "sample_player_projections.csv",
        roster_path=snapshot_dir / "flaim_roster_snapshot_sample.csv",
        roster_projection_path=interim_dir / "sample_roster_projections.csv",
        output_path=output_path,
    )

    assert saved_path.exists()

    report_text = saved_path.read_text(encoding="utf-8")

    assert "# Waiver-Wire Report" in report_text
    assert "## Weak categories" in report_text
    assert "## Top add/drop recommendations" in report_text


def test_save_latest_copy_creates_latest_report(tmp_path):
    source_path = tmp_path / "waiver_wire_report_2026_06_29.md"
    latest_path = tmp_path / "waiver_wire_report.md"

    source_path.write_text("# Waiver-Wire Report\n", encoding="utf-8")

    saved_latest_path = save_latest_copy(
        source_path=source_path,
        latest_path=latest_path,
    )

    assert saved_latest_path.exists()
    assert saved_latest_path.read_text(encoding="utf-8") == "# Waiver-Wire Report\n"


def test_calculate_file_sha256_returns_hash(tmp_path):
    test_file = tmp_path / "test.txt"
    test_file.write_text("hello", encoding="utf-8")

    file_hash = calculate_file_sha256(test_file)

    assert file_hash is not None
    assert len(file_hash) == 64


def test_file_record_includes_metadata(tmp_path):
    test_file = tmp_path / "test.txt"
    test_file.write_text("hello", encoding="utf-8")

    record = file_record(test_file)

    assert record["exists"] is True
    assert record["size_bytes"] == 5
    assert record["sha256"] is not None
    assert len(record["sha256"]) == 64


def test_git_metadata_helpers_return_expected_types():
    commit_hash = get_git_commit_hash()
    branch = get_git_branch()
    is_dirty = get_git_is_dirty()

    assert commit_hash is None or isinstance(commit_hash, str)
    assert branch is None or isinstance(branch, str)
    assert is_dirty is None or isinstance(is_dirty, bool)


def test_get_environment_metadata_contains_required_fields():
    metadata = get_environment_metadata(project_root=PROJECT_ROOT)

    assert "created_at" in metadata
    assert "project_root" in metadata
    assert "script" in metadata
    assert "command" in metadata
    assert "git_commit_hash" in metadata
    assert "git_branch" in metadata
    assert "git_is_dirty" in metadata
    assert "python_version" in metadata
    assert "python_executable" in metadata
    assert "pandas_version" in metadata
    assert "platform" in metadata

    assert metadata["project_root"] == str(PROJECT_ROOT)
    assert metadata["command"] == "python scripts/run_waiver_analysis.py"
    assert isinstance(metadata["platform"], dict)
    assert "system" in metadata["platform"]


def test_save_package_environment_exports_creates_files(tmp_path):
    exports = save_package_environment_exports(
        output_dir=tmp_path,
        date_stamp="2026_07_02",
        project_root=PROJECT_ROOT,
    )

    assert exports["pip_freeze"].exists()
    assert exports["conda_env_export"].exists()
    assert isinstance(exports["pip_freeze_success"], bool)
    assert isinstance(exports["conda_env_export_success"], bool)


def test_save_run_manifest_creates_json_with_environment_exports(tmp_path):
    raw_roster_path = tmp_path / "flaim_roster_raw_latest.json"
    raw_free_agents_path = tmp_path / "flaim_free_agents_raw_latest.json"
    free_agent_path = tmp_path / "free_agents.csv"
    free_agent_projection_path = tmp_path / "free_agent_projections.csv"
    roster_path = tmp_path / "roster.csv"
    roster_projection_path = tmp_path / "roster_projections.csv"
    report_path = tmp_path / "waiver_wire_report_2026_07_02.md"
    latest_report_path = tmp_path / "waiver_wire_report.md"
    pip_freeze_path = tmp_path / "pip_freeze_2026_07_02.txt"
    conda_env_path = tmp_path / "conda_env_2026_07_02.yml"
    manifest_path = tmp_path / "waiver_run_manifest_2026_07_02.json"

    for path in [
        raw_roster_path,
        raw_free_agents_path,
        free_agent_path,
        free_agent_projection_path,
        roster_path,
        roster_projection_path,
        report_path,
        latest_report_path,
        pip_freeze_path,
        conda_env_path,
    ]:
        path.write_text("test content", encoding="utf-8")

    environment_metadata = {
        "created_at": "2026-07-02T12:00:00+00:00",
        "project_root": str(PROJECT_ROOT),
        "script": "scripts/run_waiver_analysis.py",
        "command": "python scripts/run_waiver_analysis.py",
        "git_commit_hash": "abc123",
        "git_branch": "main",
        "git_is_dirty": False,
        "python_version": "3.11.test",
        "python_executable": "python",
        "pandas_version": "2.test",
        "platform": {
            "system": "Windows",
            "release": "test",
            "version": "test",
            "machine": "AMD64",
            "processor": "test",
            "python_implementation": "CPython",
        },
    }

    saved_path = save_run_manifest(
        manifest_path=manifest_path,
        run_date="2026_07_02",
        raw_roster_path=raw_roster_path,
        raw_free_agents_path=raw_free_agents_path,
        free_agent_path=free_agent_path,
        free_agent_projection_path=free_agent_projection_path,
        roster_path=roster_path,
        roster_projection_path=roster_projection_path,
        report_path=report_path,
        latest_report_path=latest_report_path,
        pip_freeze_path=pip_freeze_path,
        conda_env_path=conda_env_path,
        pip_freeze_success=True,
        conda_env_export_success=True,
        punt_strategy="balanced",
        weak_category_count=3,
        drop_candidate_count=5,
        top_add_count=5,
        environment_metadata=environment_metadata,
    )

    assert saved_path.exists()

    manifest = json.loads(saved_path.read_text(encoding="utf-8"))

    assert manifest["workflow"] == "waiver_analysis"
    assert manifest["environment"]["git_commit_hash"] == "abc123"
    assert manifest["environment_exports"]["pip_freeze"]["exists"] is True
    assert manifest["environment_exports"]["conda_env_export"]["exists"] is True
    assert manifest["environment_exports"]["pip_freeze_success"] is True
    assert manifest["environment_exports"]["conda_env_export_success"] is True
    assert manifest["parameters"]["punt_strategy"] == "balanced"