from datetime import datetime
from pathlib import Path
import importlib.util
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
SCRIPTS_DIR = PROJECT_ROOT / "scripts"

sys.path.insert(0, str(SRC_DIR))

from nba_fantasy.raw_capture import save_raw_json


def load_snapshot_sample_module():
    """
    Load scripts/build_flaim_snapshot_samples.py directly by file path.

    This avoids import errors when running this script directly from
    Anaconda Prompt.
    """
    module_path = SCRIPTS_DIR / "build_flaim_snapshot_samples.py"

    spec = importlib.util.spec_from_file_location(
        "build_flaim_snapshot_samples",
        module_path,
    )

    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load module from: {module_path}")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    return module


def get_date_stamp() -> str:
    """
    Return a YYYY_MM_DD date stamp for raw JSON filenames.
    """
    return datetime.now().strftime("%Y_%m_%d")


def assert_saved_nonempty(path: Path) -> None:
    """
    Confirm a saved file exists and is not empty.
    """
    if not path.exists():
        raise FileNotFoundError(f"Expected file was not created: {path}")

    if path.stat().st_size == 0:
        raise ValueError(f"Saved file is empty: {path}")


def main() -> None:
    raw_dir = PROJECT_ROOT / "data" / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)

    snapshot_module = load_snapshot_sample_module()

    roster_response = snapshot_module.ROSTER_RESPONSE
    free_agents_response = snapshot_module.FREE_AGENTS_RESPONSE

    date_stamp = get_date_stamp()

    outputs = [
        save_raw_json(
            response=roster_response,
            output_path=raw_dir / f"flaim_roster_raw_{date_stamp}.json",
        ),
        save_raw_json(
            response=free_agents_response,
            output_path=raw_dir / f"flaim_free_agents_raw_{date_stamp}.json",
        ),
        save_raw_json(
            response=roster_response,
            output_path=raw_dir / "flaim_roster_raw_latest.json",
        ),
        save_raw_json(
            response=free_agents_response,
            output_path=raw_dir / "flaim_free_agents_raw_latest.json",
        ),
    ]

    for path in outputs:
        assert_saved_nonempty(path)

    print("\nSaved raw Flaim JSON files:")

    for path in outputs:
        print(f"- {path} ({path.stat().st_size} bytes)")


if __name__ == "__main__":
    main()