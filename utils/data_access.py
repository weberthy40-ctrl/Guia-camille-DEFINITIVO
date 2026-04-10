import json
from pathlib import Path
from typing import Any

from utils.integrity import build_learning_integrity_report, read_json_status

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"



def load_json(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)



def load_json_safe(path: Path, default: Any):
    status = read_json_status(path, default=default)
    if status["status"] != "ok":
        return default
    return status["data"]



def load_camille():
    return load_json(DATA_DIR / "champions" / "camille.json")



def load_learning():
    return load_json(DATA_DIR / "learning" / "camille_learning.json")



def _fallback_learning_overview() -> dict[str, str]:
    return {
        "pt-BR": "Central de aprendizado pronta para integrar fundamentos, execução e macro da Camille.",
        "en": "Learning hub ready to integrate Camille fundamentals, execution, and macro.",
    }



def _fallback_streamers_note() -> dict[str, str]:
    return {
        "pt-BR": "Curadoria em andamento.",
        "en": "Curation in progress.",
    }


EXTRA_LEARNING_MODULES = {
    "camille_build_decision.json": {"group": "decision", "title": {"pt-BR": "Build e itemização adaptativa", "en": "Adaptive build and itemization"}},
    "camille_runes_decision.json": {"group": "decision", "title": {"pt-BR": "Decisão de runas", "en": "Rune decision"}},
    "camille_archetypes.json": {"group": "decision", "title": {"pt-BR": "Guia contra arquétipos", "en": "Archetype guide"}},
    "camille_phase_checklists.json": {"group": "decision", "title": {"pt-BR": "Checklists por fase do jogo", "en": "Phase checklists"}},
    "camille_decision_recovery.json": {"group": "decision", "title": {"pt-BR": "Recuperação de decisões ruins", "en": "Decision recovery"}},
    "camille_adaptation_layers.json": {"group": "decision", "title": {"pt-BR": "Camadas de adaptação", "en": "Adaptation layers"}},
    "camille_state_based_adjustments.json": {"group": "decision", "title": {"pt-BR": "Ajustes por estado de jogo", "en": "State-based adjustments"}},
    "camille_situational_gameplans.json": {"group": "decision", "title": {"pt-BR": "Gameplans situacionais", "en": "Situational gameplans"}},
    "camille_training_plan.json": {"group": "coaching", "title": {"pt-BR": "Plano de treino", "en": "Training plan"}},
    "camille_coach_paths.json": {"group": "coaching", "title": {"pt-BR": "Trilhas de evolução", "en": "Coaching paths"}},
    "camille_player_profiles.json": {"group": "coaching", "title": {"pt-BR": "Perfis de jogador", "en": "Player profiles"}},
    "camille_improvement_priorities.json": {"group": "coaching", "title": {"pt-BR": "Prioridades de melhoria", "en": "Improvement priorities"}},
    "camille_short_training_blocks.json": {"group": "coaching", "title": {"pt-BR": "Blocos curtos de treino", "en": "Short training blocks"}},
    "camille_review_checklists.json": {"group": "coaching", "title": {"pt-BR": "Checklists de revisão", "en": "Review checklists"}},
    "camille_common_mistakes.json": {"group": "coaching", "title": {"pt-BR": "Erros comuns", "en": "Common mistakes"}},
    "camille_mistake_corrections.json": {"group": "coaching", "title": {"pt-BR": "Correção de erros", "en": "Mistake corrections"}},
    "camille_self_review_diagnostics.json": {"group": "coaching", "title": {"pt-BR": "Diagnóstico de autoanálise", "en": "Self-review diagnostics"}},
    "camille_improvement_matrix.json": {"group": "coaching", "title": {"pt-BR": "Matriz de melhoria", "en": "Improvement matrix"}},
    "camille_game_review_triggers.json": {"group": "coaching", "title": {"pt-BR": "Gatilhos de review", "en": "Game review triggers"}},
    "camille_faq.json": {"group": "coaching", "title": {"pt-BR": "FAQ premium", "en": "Premium FAQ"}},
    "camille_advanced_interactions.json": {"group": "execution", "title": {"pt-BR": "Interações avançadas", "en": "Advanced interactions"}},
    "camille_execution_reference.json": {"group": "execution", "title": {"pt-BR": "Referência de execução", "en": "Execution reference"}},
    "camille_microtips.json": {"group": "execution", "title": {"pt-BR": "Microdicas", "en": "Microtips"}},
    "camille_glossary.json": {"group": "execution", "title": {"pt-BR": "Glossário", "en": "Glossary"}},
    "camille_practice_scenarios.json": {"group": "execution", "title": {"pt-BR": "Cenários de treino", "en": "Practice scenarios"}},
}


def _build_extra_learning_items(learning_dir: Path) -> dict[str, list[dict[str, Any]]]:
    groups: dict[str, list[dict[str, Any]]] = {"decision": [], "coaching": [], "execution": []}
    for filename, spec in EXTRA_LEARNING_MODULES.items():
        payload = load_json_safe(learning_dir / filename, {})
        if not isinstance(payload, dict) or not payload:
            continue
        overview = payload.get("overview")
        if not overview:
            continue
        groups[spec["group"]].append({
            "topic": spec["title"],
            "content": overview,
        })
    return groups



def load_learning_bundle():
    learning_dir = DATA_DIR / "learning"
    primary = load_json_safe(learning_dir / "camille_learning.json", {})
    combos_file = load_json_safe(learning_dir / "camille_combos.json", {})
    mechanics_file = load_json_safe(learning_dir / "camille_mechanics.json", {})
    macro_file = load_json_safe(learning_dir / "camille_macro.json", {})
    streamers = load_streamers()
    integrity = build_learning_integrity_report()
    extra_module_groups = _build_extra_learning_items(learning_dir)

    overview = primary.get("overview", _fallback_learning_overview())

    kit_items = primary.get("kit", [])
    mechanics_items = mechanics_file.get("mechanics") or primary.get("mechanics", [])
    combos_items = combos_file.get("combos") or primary.get("combos", [])
    execution_list = primary.get("execution", {})
    common_errors = primary.get("common_errors", {})
    decision_patterns = primary.get("decision_patterns", [])
    identity = primary.get("identity")

    game_phases = primary.get("game_phases", {})
    phases_items = [
        {"title_key": f"learning.phase_{phase}", "content": value}
        for phase, value in game_phases.items()
    ]

    macro_items = []
    for key in ["macro", "teamfight", "side_lane"]:
        content = macro_file.get(key) or primary.get(key)
        if content:
            macro_items.append({"title_key": f"learning.block_{key}", "content": content})

    matchup_general = primary.get("matchups_general", {})
    matchup_items = [
        {"title_key": f"learning.matchup_{key}", "content": value}
        for key, value in matchup_general.items()
    ]

    sections = [
        {
            "key": "foundations",
            "title_key": "learning.section_foundations",
            "description_key": "learning.section_foundations_desc",
            "blocks": [
                {"type": "text", "title_key": "learning.block_identity", "content": identity},
                {"type": "topic_list", "title_key": "learning.block_kit", "items": kit_items},
                {"type": "topic_list", "title_key": "learning.block_mechanics", "items": mechanics_items},
            ],
        },
        {
            "key": "execution",
            "title_key": "learning.section_execution",
            "description_key": "learning.section_execution_desc",
            "blocks": [
                {"type": "combo_list", "title_key": "learning.block_combos", "items": combos_items},
                {"type": "localized_list", "title_key": "learning.block_execution", "items": execution_list},
                {"type": "localized_list", "title_key": "learning.block_common_errors", "items": common_errors},
            ],
        },
        {
            "key": "gameplay",
            "title_key": "learning.section_gameplay",
            "description_key": "learning.section_gameplay_desc",
            "blocks": [
                {"type": "topic_list", "title_key": "learning.block_game_phases", "items": phases_items},
                {"type": "decision_list", "title_key": "learning.block_decision_patterns", "items": decision_patterns},
                {"type": "topic_list", "title_key": "learning.block_matchups_general", "items": matchup_items},
            ],
        },
        {
            "key": "map_play",
            "title_key": "learning.section_map_play",
            "description_key": "learning.section_map_play_desc",
            "blocks": [
                {"type": "topic_list", "title_key": "learning.block_macro_package", "items": macro_items},
            ],
        },
        {
            "key": "creators",
            "title_key": "learning.section_creators",
            "description_key": "learning.section_creators_desc",
            "blocks": [
                {"type": "creators", "title_key": "learning.streamers", "items": streamers.get("entries", [])},
            ],
        },
    ]

    if extra_module_groups["decision"]:
        sections.append({
            "key": "decision_lab",
            "title": {"pt-BR": "Biblioteca de decisão", "en": "Decision library"},
            "description": {"pt-BR": "Módulos premium de build, runas, arquétipos e adaptação para aprofundar a leitura da Camille fora das matchups individuais.", "en": "Premium modules for builds, runes, archetypes and adaptation to deepen Camille decision-making outside individual matchups."},
            "blocks": [
                {"type": "topic_list", "title": {"pt-BR": "Adaptação e leitura de jogo", "en": "Adaptation and game reading"}, "items": extra_module_groups["decision"]},
            ],
        })

    if extra_module_groups["coaching"]:
        sections.append({
            "key": "coaching_lab",
            "title": {"pt-BR": "Biblioteca de coach", "en": "Coaching library"},
            "description": {"pt-BR": "Material premium para evolução, revisão de erros, perfis de jogador e organização de treino com a Camille.", "en": "Premium material for progression, error review, player profiling and training structure with Camille."},
            "blocks": [
                {"type": "topic_list", "title": {"pt-BR": "Progressão, revisão e correção", "en": "Progression, review and correction"}, "items": extra_module_groups["coaching"]},
            ],
        })

    if extra_module_groups["execution"]:
        sections.append({
            "key": "execution_lab_plus",
            "title": {"pt-BR": "Biblioteca de execução", "en": "Execution library"},
            "description": {"pt-BR": "Referências rápidas de execução, prática e detalhes finos do kit da Camille para uso em treino e revisão.", "en": "Quick execution references, practice material and fine kit details for Camille training and review."},
            "blocks": [
                {"type": "topic_list", "title": {"pt-BR": "Execução avançada e prática", "en": "Advanced execution and practice"}, "items": extra_module_groups["execution"]},
            ],
        })

    return {
        "overview": overview,
        "streamers_note": streamers.get("source_priority_note", _fallback_streamers_note()),
        "sections": sections,
        "integrity": integrity,
    }



def load_matchup(role: str, champion_slug: str):
    return load_json(DATA_DIR / "matchups" / role / f"{champion_slug}.json")



def load_matchups_overview():
    return load_json(DATA_DIR / "meta" / "matchups_overview.json")



def load_roles_index():
    return load_json(DATA_DIR / "meta" / "roles_index.json")



def load_external_links():
    return load_json(DATA_DIR / "meta" / "external_links.json")



def load_streamers():
    return load_json_safe(DATA_DIR / "meta" / "streamers_youtubers.json", {"entries": []})
