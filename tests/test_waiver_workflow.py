from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.run_waiver_analysis import run_waiver_analysis


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