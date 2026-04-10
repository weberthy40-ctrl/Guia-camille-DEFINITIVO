from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from utils.i18n import DEFAULT_LOCALE, SUPPORTED_LOCALES, has_translation_key, load_translations
from utils.integrity import LEARNING_FILE_SPECS, read_json_status
from utils.scoring import calculate_score_from_components, difficulty_from_score

DATA_DIR = BASE_DIR / "data"
TRANSLATIONS_DIR = BASE_DIR / "translations"

REQUIRED_MATCHUP_TOP_LEVEL = [
    "identity",
    "scoring",
    "macro_view",
    "lane_phase",
    "abilities_interaction",
    "build",
    "item_winrate_system",
    "runes",
    "power_spikes",
    "common_mistakes",
    "practical_priority",
    "gameplan_complete",
    "practical_situations",
    "camille_identity_in_matchup",
    "real_difficulty",
    "metadata",
]
REQUIRED_MATCHUP_IDENTITY = [
    "champion_slug",
    "champion_name",
    "role_bucket",
    "quick_summary",
    "difficulty",
    "score",
    "enemy_identity",
    "matchup_type",
    "threat_level",
    "confidence",
]
REQUIRED_SCORING_KEYS = [
    "lane_phase_pressure",
    "gold_diff_15",
    "kill_threat",
    "matchup_winrate_pressure",
]
REQUIRED_TRANSLATION_KEYS = [
    "site.title",
    "nav.home",
    "nav.guide",
    "nav.matchups",
    "nav.learning",
    "home.title",
    "guide.title",
    "matchups.title",
    "matchup.quick_summary",
    "learning.title",
]
REQUIRED_CAMILLE_KEYS = [
    "identity",
    "summary",
    "lore_short",
    "abilities",
    "skill_order",
    "level_stats_1_20",
    "core_items",
    "most_used_full_build",
    "situational_items",
    "runes_general",
    "spikes",
    "playstyle",
    "macro_identity",
]


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)



def validate_json_file(path: Path) -> list[str]:
    try:
        load_json(path)
        return []
    except Exception as exc:
        return [f"{path}: invalid JSON ({exc})"]



def validate_matchup_file(path: Path) -> list[str]:
    errors: list[str] = []
    data = load_json(path)

    for key in REQUIRED_MATCHUP_TOP_LEVEL:
        if key not in data:
            errors.append(f"{path}: missing top-level key '{key}'")

    identity = data.get("identity", {})
    for key in REQUIRED_MATCHUP_IDENTITY:
        if key not in identity:
            errors.append(f"{path}: missing identity.{key}")

    score = identity.get("score")
    if not isinstance(score, (int, float)):
        errors.append(f"{path}: identity.score must be numeric")
    elif not (1.0 <= float(score) <= 10.0):
        errors.append(f"{path}: identity.score must be between 1.0 and 10.0")

    scoring_block = data.get("scoring", {})
    for key in REQUIRED_SCORING_KEYS:
        if key not in scoring_block:
            errors.append(f"{path}: missing scoring.{key}")
        elif not isinstance(scoring_block.get(key), (int, float)):
            errors.append(f"{path}: scoring.{key} must be numeric")

    if all(key in scoring_block and isinstance(scoring_block.get(key), (int, float)) for key in REQUIRED_SCORING_KEYS):
        calculated = calculate_score_from_components(scoring_block)
        if isinstance(score, (int, float)) and abs(calculated - float(score)) > 0.2:
            errors.append(
                f"{path}: identity.score ({score}) diverges from scoring components ({calculated})"
            )
        expected_difficulty = difficulty_from_score(float(score)) if isinstance(score, (int, float)) else None
        difficulty = identity.get("difficulty")
        if expected_difficulty and difficulty != expected_difficulty:
            errors.append(
                f"{path}: identity.difficulty should be '{expected_difficulty}' based on identity.score {score}"
            )

    path_role = path.parent.name
    role_bucket = identity.get("role_bucket")
    if role_bucket and role_bucket != path_role:
        errors.append(f"{path}: identity.role_bucket '{role_bucket}' differs from folder '{path_role}'")

    return errors



def validate_translation_files() -> list[str]:
    errors: list[str] = []
    available_files = {path.stem for path in TRANSLATIONS_DIR.glob("*.json")}
    _ = load_translations(DEFAULT_LOCALE)

    for locale in SUPPORTED_LOCALES:
        if locale not in available_files:
            errors.append(f"translations/{locale}.json: file missing")
            continue
        try:
            load_translations(locale)
        except Exception as exc:
            errors.append(f"translations/{locale}.json: failed to load ({exc})")
            continue
        for key in REQUIRED_TRANSLATION_KEYS:
            if not has_translation_key(locale, key):
                errors.append(f"translations/{locale}.json: missing required key '{key}'")

    return errors



def validate_camille_file(path: Path) -> list[str]:
    errors: list[str] = []
    data = load_json(path)
    for key in REQUIRED_CAMILLE_KEYS:
        if key not in data:
            errors.append(f"{path}: missing top-level key '{key}'")

    abilities = data.get("abilities", {})
    for key in ["passive", "q", "w", "e", "r"]:
        if key not in abilities:
            errors.append(f"{path}: missing abilities.{key}")

    if not isinstance(data.get("skill_order", []), list) or not data.get("skill_order"):
        errors.append(f"{path}: skill_order must be a non-empty list")
    if not isinstance(data.get("level_stats_1_20", []), list) or len(data.get("level_stats_1_20", [])) < 20:
        errors.append(f"{path}: level_stats_1_20 should contain at least 20 rows")

    return errors



def validate_learning_files() -> list[str]:
    errors: list[str] = []

    for filename, spec in LEARNING_FILE_SPECS.items():
        status = read_json_status(
            spec["path"],
            default={} if spec.get("expected_type") is dict else None,
            expected_type=spec.get("expected_type"),
        )
        if spec["required"] and status["status"] != "ok":
            errors.append(f"{status['path']}: required file is {status['status']}")
            continue
        if status["status"] not in {"ok", "missing"}:
            errors.append(f"{status['path']}: invalid optional file ({status['status']})")
            continue
        payload = status["data"]
        if status["status"] == "ok" and isinstance(payload, dict):
            for key in spec.get("required_keys", []):
                if key not in payload:
                    level = "required" if spec["required"] else "optional"
                    errors.append(f"{status['path']}: missing {level} key '{key}'")

    streamers_path = DATA_DIR / "meta" / "streamers_youtubers.json"
    if streamers_path.exists():
        streamers = load_json(streamers_path)
        entries = streamers.get("entries", [])
        if not isinstance(entries, list):
            errors.append(f"{streamers_path}: entries must be a list")
        else:
            for index, entry in enumerate(entries):
                if not isinstance(entry, dict):
                    errors.append(f"{streamers_path}: entries[{index}] must be an object")
                    continue
                for key in ["name", "platform", "language", "focus"]:
                    if key not in entry:
                        errors.append(f"{streamers_path}: entries[{index}] missing '{key}'")

    return errors



def validate_meta_files() -> list[str]:
    errors: list[str] = []
    for json_file in (DATA_DIR / "meta").glob("*.json"):
        errors.extend(validate_json_file(json_file))
    return errors



def validate_core_data_files() -> list[str]:
    errors: list[str] = []
    camille_path = DATA_DIR / "champions" / "camille.json"
    if camille_path.exists():
        errors.extend(validate_camille_file(camille_path))
    else:
        errors.append(f"{camille_path}: file missing")

    errors.extend(validate_learning_files())
    return errors



def main() -> None:
    errors: list[str] = []

    errors.extend(validate_translation_files())
    errors.extend(validate_core_data_files())
    errors.extend(validate_meta_files())

    matchup_root = DATA_DIR / "matchups"
    matchup_files = list(matchup_root.rglob("*.json"))
    for json_file in matchup_files:
        errors.extend(validate_matchup_file(json_file))

    if errors:
        print("Validation failed:")
        for error in errors:
            print(f" - {error}")
        raise SystemExit(1)

    print(f"Validation passed: {len(matchup_files)} matchup files checked.")
    print(f"Locales checked: {', '.join(SUPPORTED_LOCALES)}")
    print("Learning bundle specs checked.")


if __name__ == "__main__":
    main()
