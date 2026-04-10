from __future__ import annotations

import json
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from utils.integrity import (  # noqa: E402
    build_expected_files_manifest,
    build_learning_integrity_report,
    write_json,
)
from utils.scoring import clamp_score, difficulty_from_score

DATA_DIR = BASE_DIR / "data"
MATCHUPS_DIR = DATA_DIR / "matchups"
META_DIR = DATA_DIR / "meta"
OVERVIEW_FILE = META_DIR / "matchups_overview.json"
ROLES_FILE = META_DIR / "roles_index.json"
LEARNING_STATUS_FILE = META_DIR / "learning_bundle_status.json"
EXPECTED_FILES_FILE = META_DIR / "expected_files_manifest.json"



def load_json(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)



def build_matchups_overview() -> dict:
    overview: dict[str, dict[str, list[dict]]] = {}
    for role_dir in sorted(MATCHUPS_DIR.iterdir()):
        if not role_dir.is_dir():
            continue

        groups = {"suggest_ban": [], "hard": [], "medium": [], "easy": []}
        for file_path in sorted(role_dir.glob("*.json")):
            data = load_json(file_path)
            identity = data["identity"]
            score = clamp_score(identity["score"])
            bucket = difficulty_from_score(score)
            groups[bucket].append(
                {
                    "champion_slug": identity["champion_slug"],
                    "champion_name": identity["champion_name"],
                    "score": score,
                    "role_bucket": identity["role_bucket"],
                    "difficulty": identity["difficulty"],
                    "confidence": identity.get("confidence", "medium"),
                }
            )

        for bucket_items in groups.values():
            bucket_items.sort(key=lambda item: (-item["score"], item["champion_name"]))
        overview[role_dir.name] = groups
    return overview



def build_roles_index() -> dict:
    roles_index: dict[str, dict] = {}
    for role_dir in sorted(MATCHUPS_DIR.iterdir()):
        if not role_dir.is_dir():
            continue

        champions: list[dict] = []
        for file_path in sorted(role_dir.glob("*.json")):
            data = load_json(file_path)
            identity = data["identity"]
            champions.append(
                {
                    "slug": identity["champion_slug"],
                    "name": identity["champion_name"],
                    "score": clamp_score(identity["score"]),
                    "difficulty": identity["difficulty"],
                }
            )

        champions.sort(key=lambda item: item["name"])
        roles_index[role_dir.name] = {
            "count": len(champions),
            "champions": champions,
        }
    return roles_index



def main() -> None:
    overview = build_matchups_overview()
    roles_index = build_roles_index()
    learning_status = build_learning_integrity_report()
    expected_files = build_expected_files_manifest()

    write_json(OVERVIEW_FILE, overview)
    write_json(ROLES_FILE, roles_index)
    write_json(LEARNING_STATUS_FILE, learning_status)
    write_json(EXPECTED_FILES_FILE, expected_files)

    print(f"Overview index rebuilt at {OVERVIEW_FILE}")
    print(f"Roles index rebuilt at {ROLES_FILE}")
    print(f"Learning bundle status written to {LEARNING_STATUS_FILE}")
    print(f"Expected files manifest written to {EXPECTED_FILES_FILE}")


if __name__ == "__main__":
    main()
