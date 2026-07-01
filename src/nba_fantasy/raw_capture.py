"""
Raw data capture helpers.

These helpers save and load raw connector responses as JSON files.
The goal is to preserve the original connector output before transforming
it into analysis-ready CSV snapshots.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def save_raw_json(
    response: dict[str, Any],
    output_path: str | Path,
) -> Path:
    """
    Save a raw connector response as JSON.

    Raises
    ------
    ValueError
        If the response is empty or not a dictionary.
    """
    if not isinstance(response, dict):
        raise ValueError("Raw response must be a dictionary.")

    if not response:
        raise ValueError("Raw response is empty.")

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    json_text = json.dumps(
        response,
        indent=2,
        ensure_ascii=False,
    )

    if not json_text.strip():
        raise ValueError("JSON serialization produced empty text.")

    output_path.write_text(
        json_text,
        encoding="utf-8",
    )

    return output_path


def load_raw_json(input_path: str | Path) -> dict[str, Any]:
    """
    Load a raw connector response from JSON.
    """
    input_path = Path(input_path)

    if not input_path.exists():
        raise FileNotFoundError(f"Raw JSON file does not exist: {input_path}")

    if input_path.stat().st_size == 0:
        raise ValueError(f"Raw JSON file is empty: {input_path}")

    return json.loads(input_path.read_text(encoding="utf-8"))