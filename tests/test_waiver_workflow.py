import json
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.run_waiver_analysis import (
    calculate_file_sha256,
    file_record,
    run_waiver_analysis,
    save_latest_copy,
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


def test_save_run_manifest_creates_json_with_hashes(tmp_path):
    raw_roster_path = tmp_path / "flaim_roster_raw_latest.json"
    raw_free_agents_path = tmp_path / "flaim_free_agents_raw_latest.json"
    free_agent_path = tmp_path / "free_agents.csv"
    free_agent_projection_path = tmp_path / "free_agent_projections.csv"
    roster_path = tmp_path / "roster.csv"
    roster_projection_path = tmp_path / "roster_projections.csv"
    report_path = tmp_path / "waiver_wire_report_2026_07_02.md"
    latest_report_path = tmp_path / "waiver_wire_report.md"
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
    ]:
        path.write_text("test content", encoding="utf-8")

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
        punt_strategy="balanced",
        weak_category_count=3,
        drop_candidate_count=5,
        top_add_count=5,
    )

    assert saved_path.exists()

    manifest = json.loads(saved_path.read_text(encoding="utf-8"))

    assert manifest["workflow"] == "waiver_analysis"
    assert manifest["raw_inputs"]["raw_roster_json"]["exists"] is True
    assert manifest["raw_inputs"]["raw_roster_json"]["sha256"] is not None
    assert len(manifest["raw_inputs"]["raw_roster_json"]["sha256"]) == 64
    assert manifest["parameters"]["punt_strategy"] == "balanced"