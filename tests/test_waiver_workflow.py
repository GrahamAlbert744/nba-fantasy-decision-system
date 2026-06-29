from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.run_waiver_analysis import (
    run_waiver_analysis,
    save_latest_copy,
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