from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.run_waiver_analysis import (
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


def test_save_run_manifest_creates_json(tmp_path):
    manifest_path = tmp_path / "waiver_run_manifest_2026_06_29.json"

    saved_path = save_run_manifest(
        manifest_path=manifest_path,
        run_date="2026_06_29",
        free_agent_path=tmp_path / "free_agents.csv",
        free_agent_projection_path=tmp_path / "free_agent_projections.csv",
        roster_path=tmp_path / "roster.csv",
        roster_projection_path=tmp_path / "roster_projections.csv",
        report_path=tmp_path / "waiver_wire_report_2026_06_29.md",
        latest_report_path=tmp_path / "waiver_wire_report.md",
        punt_strategy="balanced",
        weak_category_count=3,
        drop_candidate_count=5,
        top_add_count=5,
    )

    assert saved_path.exists()

    manifest_text = saved_path.read_text(encoding="utf-8")

    assert '"workflow": "waiver_analysis"' in manifest_text
    assert '"punt_strategy": "balanced"' in manifest_text
    assert '"weak_category_count": 3' in manifest_text
    assert '"drop_candidate_count": 5' in manifest_text
    assert '"top_add_count": 5' in manifest_text


def test_save_run_manifest_records_inputs_and_outputs(tmp_path):
    manifest_path = tmp_path / "waiver_run_manifest_2026_06_29.json"

    saved_path = save_run_manifest(
        manifest_path=manifest_path,
        run_date="2026_06_29",
        free_agent_path=tmp_path / "free_agents.csv",
        free_agent_projection_path=tmp_path / "free_agent_projections.csv",
        roster_path=tmp_path / "roster.csv",
        roster_projection_path=tmp_path / "roster_projections.csv",
        report_path=tmp_path / "waiver_wire_report_2026_06_29.md",
        latest_report_path=tmp_path / "waiver_wire_report.md",
        punt_strategy="balanced",
        weak_category_count=3,
        drop_candidate_count=5,
        top_add_count=5,
    )

    manifest_text = saved_path.read_text(encoding="utf-8")

    assert "free_agent_snapshot" in manifest_text
    assert "free_agent_projection_file" in manifest_text
    assert "roster_snapshot" in manifest_text
    assert "roster_projection_file" in manifest_text
    assert "dated_report" in manifest_text
    assert "latest_report" in manifest_text