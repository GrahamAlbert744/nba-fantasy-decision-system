from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = PROJECT_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
INTERIM_DIR = DATA_DIR / "interim"
PROCESSED_DIR = DATA_DIR / "processed"
OUTPUT_DIR = DATA_DIR / "outputs"
LEAGUE_SNAPSHOT_DIR = DATA_DIR / "league_snapshots"
DRAFT_BOARD_DIR = DATA_DIR / "draft_boards"

LEAGUE_CONTEXT = {
    "platform": "yahoo",
    "sport": "basketball",
    "league_id": "466.l.3706",
    "team_id": "9",
    "season_year": 2025,
    "league_name": "Lou Williams Memorial League",
    "team_name": "Dame Time Management",
}
