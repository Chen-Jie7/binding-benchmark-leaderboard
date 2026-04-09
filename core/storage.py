from __future__ import annotations

import json
from pathlib import Path

from filelock import FileLock

STORAGE_PATH = Path(__file__).parent.parent / "data" / "submissions.json"
LOCK_PATH = STORAGE_PATH.with_suffix(".lock")


def load_submissions() -> list[dict]:
    """Load all submissions from the JSON file."""
    if not STORAGE_PATH.exists():
        return []
    with open(STORAGE_PATH) as f:
        data = json.load(f)
    return data.get("submissions", [])


def save_submission(entry: dict) -> None:
    """Append a submission entry to the JSON file (thread-safe)."""
    STORAGE_PATH.parent.mkdir(parents=True, exist_ok=True)
    with FileLock(LOCK_PATH):
        submissions = load_submissions()
        submissions.append(entry)
        with open(STORAGE_PATH, "w") as f:
            json.dump({"submissions": submissions}, f, indent=2)
