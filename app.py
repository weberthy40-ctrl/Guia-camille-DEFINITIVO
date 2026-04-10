from pathlib import Path
from flask import Flask, abort, render_template, request, url_for

from utils import (
    get_locale,
    get_supported_locales,
    translate_key,
    localize_value,
    get_champion_icon_payload,
    localize_term,
    matchup_field_label,
)
from utils.data_access import (
    load_camille,
    load_learning_bundle,
    load_matchup,
    load_matchups_overview,
    load_roles_index,
    load_external_links,
)

BASE_DIR = Path(__file__).resolve().parent
app = Flask(__name__)

ROLE_LABEL_KEYS = {
    "all": "matchups.role_all",
    "top": "matchups.role_top",
    "jungle": "matchups.role_jungle",
    "mid": "matchups.role_mid",
    "adc": "matchups.role_adc",
    "support": "matchups.role_support",
}
ROLE_SEQUENCE = ["all", "top", "jungle", "mid", "adc", "support"]
DIFFICULTY_LABEL_KEYS = {
    "suggest_ban": "matchups.suggest_ban",
    "hard": "matchups.hard",
    "medium": "matchups.medium",
    "easy": "matchups.easy",
}

TOP_DISPLAY_POOL = {
    "aatrox", "akali", "ambessa", "anivia", "chogath", "darius", "dr-mundo", "fiora", "gangplank",
    "garen", "gnar", "gragas", "gwen", "heimerdinger", "illaoi", "irelia", "jax", "jayce", "kayle",
    "kennen", "kled", "ksante", "malphite", "mordekaiser", "nasus", "olaf", "ornn", "pantheon", "poppy",
    "quinn", "renekton", "riven", "rumble", "ryze", "sett", "shen", "singed", "sion", "swain", "tahm-kench",
    "teemo", "trundle", "tryndamere", "urgot", "varus", "vayne", "vladimir", "volibear", "warwick", "wukong",
    "yone", "yorick", "zac"
}


def filter_overview_for_display(overview: dict) -> dict:
    filtered = {}
    for role, groups in overview.items():
        filtered[role] = {}
        for difficulty, items in groups.items():
            if role == "top":
                filtered[role][difficulty] = [item for item in items if item.get("champion_slug") in TOP_DISPLAY_POOL]
            else:
                filtered[role][difficulty] = list(items)
    return filtered

LANGUAGE_LABEL_KEYS = {
    "pt-BR": "nav.language_pt_br",
    "en": "nav.language_en",
}


def build_overview_with_all(overview: dict) -> dict:
    merged = {
        role: {difficulty: list(items) for difficulty, items in groups.items()}
        for role, groups in overview.items()
    }
    all_groups = {difficulty: [] for difficulty in DIFFICULTY_LABEL_KEYS}

    for role in ["top", "jungle", "mid", "adc", "support"]:
        for difficulty in DIFFICULTY_LABEL_KEYS:
            items = overview.get(role, {}).get(difficulty, [])
            for item in items:
                enriched = dict(item)
                enriched["route_role"] = role
                all_groups[difficulty].append(enriched)

    for difficulty, items in all_groups.items():
        items.sort(key=lambda item: (-float(item.get("score", 0)), item.get("champion_name", "")))

    merged["all"] = all_groups
    return merged


@app.context_processor
def inject_globals():
    locale = get_locale()
    available_languages = [
        {"code": code, "label_key": LANGUAGE_LABEL_KEYS.get(code, "nav.language")}
        for code in get_supported_locales()
    ]

    def t(key: str, **kwargs):
        return translate_key(key, locale, **kwargs)

    def loc(value):
        return localize_value(value, locale)

    def lang_url(**kwargs):
        args = request.args.to_dict(flat=True)
        args.update(kwargs)
        endpoint = request.endpoint or "home"
        view_args = request.view_args or {}
        return url_for(endpoint, **view_args, **args)

    def asset_or_placeholder(slug: str):
        payload = get_champion_icon_payload(slug)
        src = payload["src"]
        if isinstance(src, str) and src.startswith(("http://", "https://")):
            return src
        return url_for("static", filename=src)

    def champion_icon(slug: str):
        payload = get_champion_icon_payload(slug)
        src = payload["src"]
        fallback = payload["fallback"]
        if isinstance(src, str) and not src.startswith(("http://", "https://")):
            src = url_for("static", filename=src)
        if isinstance(fallback, str) and not fallback.startswith(("http://", "https://")):
            fallback = url_for("static", filename=fallback)
        return {**payload, "src": src, "fallback": fallback}

    def term(value):
        return localize_term(value, locale)

    def matchup_label(key: str):
        return matchup_field_label(key, locale)

    return {
        "t": t,
        "loc": loc,
        "lang_url": lang_url,
        "current_lang": locale,
        "role_label_keys": ROLE_LABEL_KEYS,
        "difficulty_label_keys": DIFFICULTY_LABEL_KEYS,
        "role_sequence": ROLE_SEQUENCE,
        "available_languages": available_languages,
        "asset_or_placeholder": asset_or_placeholder,
        "champion_icon": champion_icon,
        "term": term,
        "matchup_label": matchup_label,
    }


@app.route("/")
def home():
    camille = load_camille()
    links = load_external_links().get("camille", {})
    return render_template("home.html", camille=camille, links=links, page_title_key="home.title")


@app.route("/guide")
def champion_guide():
    camille = load_camille()
    return render_template("champion_guide.html", camille=camille, page_title_key="guide.title")


@app.route("/matchups")
def matchups_overview():
    overview = build_overview_with_all(filter_overview_for_display(load_matchups_overview()))
    roles_index = load_roles_index()
    active_role = request.args.get("role", "all")
    if active_role not in ROLE_SEQUENCE:
        active_role = "all"
    return render_template(
        "matchups_overview.html",
        overview=overview,
        roles_index=roles_index,
        active_role=active_role,
        overview_roles=ROLE_SEQUENCE,
        page_title_key="matchups.title",
    )


@app.route("/matchups/<role>/<champion_slug>")
def matchup_detail(role: str, champion_slug: str):
    if role not in {"top", "jungle", "mid", "adc", "support"}:
        abort(404)
    try:
        matchup = load_matchup(role, champion_slug)
    except FileNotFoundError:
        abort(404)
    return render_template("matchup_detail.html", matchup=matchup, role=role, page_title_key="matchup.title")


@app.route("/learning")
def learning():
    learning_data = load_learning_bundle()
    return render_template("learning.html", learning=learning_data, page_title_key="learning.title")


if __name__ == "__main__":
    app.run(debug=True)
