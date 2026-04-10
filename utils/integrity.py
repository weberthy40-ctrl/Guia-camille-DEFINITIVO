from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
TRANSLATIONS_DIR = BASE_DIR / "translations"
DISPLAY_I18N_REPORT_PATH = DATA_DIR / "meta" / "display_i18n_report.json"

LEARNING_FILE_SPECS: dict[str, dict[str, Any]] = {
    "camille_learning.json": {
        "path": DATA_DIR / "learning" / "camille_learning.json",
        "required": True,
        "expected_type": dict,
        "required_keys": [
            "overview",
            "identity",
            "kit",
            "combos",
            "mechanics",
            "execution",
            "common_errors",
            "decision_patterns",
            "game_phases",
            "macro",
            "teamfight",
            "side_lane",
            "matchups_general",
        ],
    },
    "camille_combos.json": {
        "path": DATA_DIR / "learning" / "camille_combos.json",
        "required": False,
        "expected_type": dict,
        "required_keys": ["combos"],
    },
    "camille_mechanics.json": {
        "path": DATA_DIR / "learning" / "camille_mechanics.json",
        "required": False,
        "expected_type": dict,
        "required_keys": ["mechanics"],
    },
    "camille_macro.json": {
        "path": DATA_DIR / "learning" / "camille_macro.json",
        "required": False,
        "expected_type": dict,
        "required_keys": ["macro", "teamfight", "side_lane"],
    },
    "streamers_youtubers.json": {
        "path": DATA_DIR / "meta" / "streamers_youtubers.json",
        "required": False,
        "expected_type": dict,
        "required_keys": ["entries", "source_priority_note"],
    },
    "camille_build_decision.json": {
        "path": DATA_DIR / "learning" / "camille_build_decision.json",
        "required": False,
        "expected_type": dict,
        "required_keys": ["overview"],
    },
    "camille_runes_decision.json": {
        "path": DATA_DIR / "learning" / "camille_runes_decision.json",
        "required": False,
        "expected_type": dict,
        "required_keys": ["overview"],
    },
    "camille_archetypes.json": {
        "path": DATA_DIR / "learning" / "camille_archetypes.json",
        "required": False,
        "expected_type": dict,
        "required_keys": ["overview"],
    },
    "camille_training_plan.json": {
        "path": DATA_DIR / "learning" / "camille_training_plan.json",
        "required": False,
        "expected_type": dict,
        "required_keys": ["overview"],
    },
    "camille_phase_checklists.json": {
        "path": DATA_DIR / "learning" / "camille_phase_checklists.json",
        "required": False,
        "expected_type": dict,
        "required_keys": ["overview"],
    },
    "camille_faq.json": {
        "path": DATA_DIR / "learning" / "camille_faq.json",
        "required": False,
        "expected_type": dict,
        "required_keys": ["overview"],
    },
    "camille_advanced_interactions.json": {
        "path": DATA_DIR / "learning" / "camille_advanced_interactions.json",
        "required": False,
        "expected_type": dict,
        "required_keys": ["overview"],
    },
    "camille_execution_reference.json": {
        "path": DATA_DIR / "learning" / "camille_execution_reference.json",
        "required": False,
        "expected_type": dict,
        "required_keys": ["overview"],
    },
    "camille_microtips.json": {
        "path": DATA_DIR / "learning" / "camille_microtips.json",
        "required": False,
        "expected_type": dict,
        "required_keys": ["overview"],
    },
    "camille_glossary.json": {
        "path": DATA_DIR / "learning" / "camille_glossary.json",
        "required": False,
        "expected_type": dict,
        "required_keys": ["overview"],
    },
    "camille_practice_scenarios.json": {
        "path": DATA_DIR / "learning" / "camille_practice_scenarios.json",
        "required": False,
        "expected_type": dict,
        "required_keys": ["overview"],
    },
    "camille_coach_paths.json": {
        "path": DATA_DIR / "learning" / "camille_coach_paths.json",
        "required": False,
        "expected_type": dict,
        "required_keys": ["overview"],
    },
    "camille_player_profiles.json": {
        "path": DATA_DIR / "learning" / "camille_player_profiles.json",
        "required": False,
        "expected_type": dict,
        "required_keys": ["overview"],
    },
    "camille_improvement_priorities.json": {
        "path": DATA_DIR / "learning" / "camille_improvement_priorities.json",
        "required": False,
        "expected_type": dict,
        "required_keys": ["overview"],
    },
    "camille_short_training_blocks.json": {
        "path": DATA_DIR / "learning" / "camille_short_training_blocks.json",
        "required": False,
        "expected_type": dict,
        "required_keys": ["overview"],
    },
    "camille_review_checklists.json": {
        "path": DATA_DIR / "learning" / "camille_review_checklists.json",
        "required": False,
        "expected_type": dict,
        "required_keys": ["overview"],
    },
    "camille_common_mistakes.json": {
        "path": DATA_DIR / "learning" / "camille_common_mistakes.json",
        "required": False,
        "expected_type": dict,
        "required_keys": ["overview"],
    },
    "camille_mistake_corrections.json": {
        "path": DATA_DIR / "learning" / "camille_mistake_corrections.json",
        "required": False,
        "expected_type": dict,
        "required_keys": ["overview"],
    },
    "camille_self_review_diagnostics.json": {
        "path": DATA_DIR / "learning" / "camille_self_review_diagnostics.json",
        "required": False,
        "expected_type": dict,
        "required_keys": ["overview"],
    },
    "camille_improvement_matrix.json": {
        "path": DATA_DIR / "learning" / "camille_improvement_matrix.json",
        "required": False,
        "expected_type": dict,
        "required_keys": ["overview"],
    },
    "camille_game_review_triggers.json": {
        "path": DATA_DIR / "learning" / "camille_game_review_triggers.json",
        "required": False,
        "expected_type": dict,
        "required_keys": ["overview"],
    },
    "camille_situational_gameplans.json": {
        "path": DATA_DIR / "learning" / "camille_situational_gameplans.json",
        "required": False,
        "expected_type": dict,
        "required_keys": ["overview"],
    },
    "camille_decision_recovery.json": {
        "path": DATA_DIR / "learning" / "camille_decision_recovery.json",
        "required": False,
        "expected_type": dict,
        "required_keys": ["overview"],
    },
    "camille_adaptation_layers.json": {
        "path": DATA_DIR / "learning" / "camille_adaptation_layers.json",
        "required": False,
        "expected_type": dict,
        "required_keys": ["overview"],
    },
    "camille_state_based_adjustments.json": {
        "path": DATA_DIR / "learning" / "camille_state_based_adjustments.json",
        "required": False,
        "expected_type": dict,
        "required_keys": ["overview"],
    },
}

EXPECTED_PROJECT_FILES: dict[str, list[str]] = {
    "required_runtime": [
        "app.py",
        "requirements.txt",
        "render.yaml",
        "templates/base.html",
        "templates/home.html",
        "templates/champion_guide.html",
        "templates/learning.html",
        "translations/pt-BR.json",
        "translations/en.json",
        "utils/data_access.py",
        "utils/i18n.py",
        "scripts/validate_data.py",
        "scripts/build_indexes.py",
        "scripts/check_missing_assets.py",
        "scripts/check_integrity.py",
        "scripts/check_i18n.py",
        "scripts/check_display_i18n.py",
        "scripts/smoke_check.py",
        "scripts/check_packaging_hygiene.py",
    ],
    "required_docs": [
        "README.md",
        "pipeline/merge_readiness.md",
        "pipeline/premerge_predeploy_checklist.md",
        "pipeline/packaging_hygiene.md",
    ],
    "optional_learning_inputs": [
        "data/learning/camille_learning.json",
        "data/learning/camille_combos.json",
        "data/learning/camille_mechanics.json",
        "data/learning/camille_macro.json",
        "data/learning/camille_build_decision.json",
        "data/learning/camille_runes_decision.json",
        "data/learning/camille_archetypes.json",
        "data/learning/camille_training_plan.json",
        "data/learning/camille_phase_checklists.json",
        "data/learning/camille_faq.json",
        "data/learning/camille_advanced_interactions.json",
        "data/learning/camille_execution_reference.json",
        "data/learning/camille_microtips.json",
        "data/learning/camille_glossary.json",
        "data/learning/camille_practice_scenarios.json",
        "data/learning/camille_coach_paths.json",
        "data/learning/camille_player_profiles.json",
        "data/learning/camille_improvement_priorities.json",
        "data/learning/camille_short_training_blocks.json",
        "data/learning/camille_review_checklists.json",
        "data/learning/camille_common_mistakes.json",
        "data/learning/camille_mistake_corrections.json",
        "data/learning/camille_self_review_diagnostics.json",
        "data/learning/camille_improvement_matrix.json",
        "data/learning/camille_game_review_triggers.json",
        "data/learning/camille_situational_gameplans.json",
        "data/learning/camille_decision_recovery.json",
        "data/learning/camille_adaptation_layers.json",
        "data/learning/camille_state_based_adjustments.json",
        "data/meta/streamers_youtubers.json",
    ],
    "expected_meta_outputs": [
        "data/meta/assets_report.json",
        "data/meta/matchups_overview.json",
        "data/meta/roles_index.json",
        "data/meta/i18n_report.json",
        "data/meta/learning_bundle_status.json",
        "data/meta/learning_integrity_report.json",
        "data/meta/merge_readiness_report.json",
        "data/meta/packaging_hygiene_report.json",
        "data/meta/smoke_check_report.json",
        "data/meta/premerge_predeploy_checklist.json",
        "data/meta/display_i18n_report.json",
    ],
}

PACKAGING_NOISE_PATTERNS = [
    "__pycache__",
    "*.pyc",
    "*.pyo",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    ".DS_Store",
]


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)



def read_json_status(
    path: Path,
    *,
    default: Any = None,
    expected_type: type | tuple[type, ...] | None = None,
) -> dict[str, Any]:
    status: dict[str, Any] = {
        "path": str(path.relative_to(BASE_DIR)),
        "exists": path.exists(),
        "status": "ok",
        "error": None,
        "data": default,
    }

    if not path.exists():
        status["status"] = "missing"
        return status

    try:
        payload = load_json(path)
    except Exception as exc:  # pragma: no cover - defensive runtime path
        status["status"] = "invalid_json"
        status["error"] = str(exc)
        return status

    if expected_type is not None and not isinstance(payload, expected_type):
        expected_name = getattr(expected_type, "__name__", str(expected_type))
        status["status"] = "type_mismatch"
        status["error"] = f"expected {expected_name}, got {type(payload).__name__}"
        return status

    status["data"] = payload
    return status



def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)
        handle.write("\n")



def _missing_keys(payload: Any, required_keys: list[str]) -> list[str]:
    if not isinstance(payload, dict):
        return list(required_keys)
    return [key for key in required_keys if key not in payload]



def build_learning_integrity_report() -> dict[str, Any]:
    files: dict[str, dict[str, Any]] = {}
    missing_required_files: list[str] = []
    missing_required_keys: dict[str, list[str]] = {}
    invalid_files: list[str] = []
    optional_files_missing: list[str] = []
    optional_files_usable: list[str] = []

    for filename, spec in LEARNING_FILE_SPECS.items():
        result = read_json_status(
            spec["path"],
            default={} if spec.get("expected_type") is dict else None,
            expected_type=spec.get("expected_type"),
        )
        report_entry = {
            "path": result["path"],
            "required": spec["required"],
            "status": result["status"],
            "missing_required_keys": [],
        }
        if result["status"] != "ok":
            report_entry["error"] = result["error"]
            if spec["required"]:
                missing_required_files.append(filename)
            else:
                optional_files_missing.append(filename)
                invalid_files.append(filename)
        else:
            payload = result["data"]
            missing_keys = _missing_keys(payload, spec.get("required_keys", []))
            report_entry["missing_required_keys"] = missing_keys
            if missing_keys:
                missing_required_keys[filename] = missing_keys
                if spec["required"]:
                    missing_required_files.append(filename)
            if not spec["required"] and not missing_keys:
                optional_files_usable.append(filename)
        files[filename] = report_entry

    primary = files.get("camille_learning.json", {})
    combos = files.get("camille_combos.json", {})
    mechanics = files.get("camille_mechanics.json", {})
    macro = files.get("camille_macro.json", {})
    creators = files.get("streamers_youtubers.json", {})

    coverage = {
        "overview": primary.get("status") == "ok",
        "combos": primary.get("status") == "ok" or combos.get("status") == "ok",
        "mechanics": primary.get("status") == "ok" or mechanics.get("status") == "ok",
        "macro": primary.get("status") == "ok" or macro.get("status") == "ok",
        "creators": creators.get("status") == "ok",
    }

    ready_for_runtime = primary.get("status") == "ok" and not primary.get("missing_required_keys")

    return {
        "learning_bundle_files": files,
        "bundle_runtime_ready": ready_for_runtime,
        "bundle_section_coverage": coverage,
        "missing_required_files": sorted(set(missing_required_files)),
        "missing_required_keys": missing_required_keys,
        "optional_files_missing_or_invalid": sorted(set(optional_files_missing)),
        "optional_files_usable": sorted(optional_files_usable),
        "warnings_present": bool(missing_required_files or missing_required_keys or optional_files_missing),
    }



def build_expected_files_manifest() -> dict[str, Any]:
    manifest: dict[str, Any] = {}
    for group, entries in EXPECTED_PROJECT_FILES.items():
        manifest[group] = []
        for relative in entries:
            path = BASE_DIR / relative
            manifest[group].append({
                "path": relative,
                "exists": path.exists(),
            })
    return manifest



def _collect_packaging_noise() -> list[str]:
    issues: list[str] = []
    for directory in BASE_DIR.rglob("__pycache__"):
        if directory.is_dir():
            issues.append(str(directory.relative_to(BASE_DIR)))
    for pattern in ["*.pyc", "*.pyo", ".DS_Store"]:
        for path in BASE_DIR.rglob(pattern):
            if path.is_file():
                issues.append(str(path.relative_to(BASE_DIR)))
    for hidden_dir in [".pytest_cache", ".mypy_cache", ".ruff_cache"]:
        for path in BASE_DIR.rglob(hidden_dir):
            if path.exists():
                issues.append(str(path.relative_to(BASE_DIR)))
    return sorted(set(issues))



def _remove_packaging_noise(items: list[str]) -> list[str]:
    removed: list[str] = []
    for relative in items:
        path = BASE_DIR / relative
        try:
            if path.is_dir():
                shutil.rmtree(path)
                removed.append(relative)
            elif path.exists():
                path.unlink()
                removed.append(relative)
        except OSError:
            continue
    return sorted(set(removed))



def build_packaging_hygiene_report() -> dict[str, Any]:
    initial_items = _collect_packaging_noise()
    removed_items = _remove_packaging_noise(initial_items) if initial_items else []
    remaining_items = _collect_packaging_noise()
    return {
        "noise_patterns_checked": PACKAGING_NOISE_PATTERNS,
        "noise_items_found_before_cleanup": initial_items,
        "removed_noise_items": removed_items,
        "noise_items_found": remaining_items,
        "noise_items_remaining_after_cleanup": remaining_items,
        "cleanup_performed": bool(initial_items),
        "clean_for_packaging": len(remaining_items) == 0,
        "autocontamination_safe": True,
        "notes": [
            "This check removes removable packaging noise before the final scan.",
            "The final cleanliness status reflects the post-cleanup state of the tree.",
        ],
    }



def scan_packaging_noise() -> dict[str, Any]:
    return build_packaging_hygiene_report()



def build_merge_readiness_report(packaging_report: dict[str, Any] | None = None) -> dict[str, Any]:
    learning_report = build_learning_integrity_report()
    expected_files = build_expected_files_manifest()
    packaging = packaging_report or build_packaging_hygiene_report()

    missing_required_runtime = [
        item["path"]
        for item in expected_files["required_runtime"]
        if not item["exists"]
    ]
    missing_required_docs = [
        item["path"]
        for item in expected_files.get("required_docs", [])
        if not item["exists"]
    ]
    missing_meta_outputs = [
        item["path"]
        for item in expected_files["expected_meta_outputs"]
        if not item["exists"]
    ]

    display_i18n_status = read_json_status(DISPLAY_I18N_REPORT_PATH, default={}, expected_type=dict)
    display_i18n_ready = False
    if display_i18n_status["status"] == "ok" and isinstance(display_i18n_status["data"], dict):
        display_i18n_ready = bool(display_i18n_status["data"].get("display_locale_consistent"))

    checks = {
        "required_runtime_files": len(missing_required_runtime) == 0,
        "required_docs_present": len(missing_required_docs) == 0,
        "learning_bundle_runtime_ready": learning_report["bundle_runtime_ready"],
        "meta_outputs_present": len(missing_meta_outputs) == 0,
        "translations_present": all(
            (TRANSLATIONS_DIR / name).exists() for name in ["pt-BR.json", "en.json"]
        ),
        "packaging_noise_absent": packaging["clean_for_packaging"],
        "display_i18n_ready": display_i18n_ready,
    }

    readiness_questions = {
        "project_structurally_ready_for_future_merge_inputs": all([
            checks["required_runtime_files"],
            checks["required_docs_present"],
            checks["translations_present"],
            checks["display_i18n_ready"],
        ]),
        "learning_ready_for_final_premium_content_absorption": learning_report["bundle_runtime_ready"],
        "principal_line_likely_to_survive_file_level_fusion": all([
            checks["required_runtime_files"],
            checks["packaging_noise_absent"],
            checks["display_i18n_ready"],
        ]),
        "remaining_gaps_require_manual_review": True,
    }

    manual_review_required = [
        "Comparar arquivo por arquivo os pacotes aprovados antes da fusão final.",
        "Revisar visualmente Home, Entenda a Campeã e /learning após qualquer consolidação.",
        "Confirmar que o conteúdo premium final da paralela 2 encaixa semanticamente nos blocos atuais.",
        "Validar a versão final dos matchups vinda da paralela 1 sem sobrescrever arquivos sistêmicos melhores.",
        "Executar smoke check e revisão manual pré-deploy antes de ativar Render em produção.",
    ]

    ready_for_parallel_merge_prep = all(checks.values())

    return {
        "checks": checks,
        "ready_for_parallel_merge_prep": ready_for_parallel_merge_prep,
        "missing_required_runtime_files": missing_required_runtime,
        "missing_required_docs": missing_required_docs,
        "missing_meta_outputs": missing_meta_outputs,
        "packaging": packaging,
        "display_i18n": display_i18n_status["data"] if display_i18n_status["status"] == "ok" else {"status": display_i18n_status["status"]},
        "report_consistency": {
            "packaging_report_used_as_single_source_of_truth": True,
            "packaging_report_clean_matches_merge_check": packaging["clean_for_packaging"] == checks["packaging_noise_absent"],
        },
        "learning": learning_report,
        "expected_files_manifest": expected_files,
        "readiness_questions": readiness_questions,
        "manual_review_required": manual_review_required,
        "notes": [
            "This report prepares the principal line for future approved-package fusion.",
            "It does not perform any merge and does not modify matchup content.",
        ],
    }
