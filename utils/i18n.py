from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any

try:
    from flask import request
except Exception:  # pragma: no cover - allows scripts to run without Flask installed
    request = None

BASE_DIR = Path(__file__).resolve().parent.parent
TRANSLATIONS_DIR = BASE_DIR / "translations"
DEFAULT_LOCALE = "pt-BR"
LOCALE_ALIASES = {
    "pt": "pt-BR",
    "pt-br": "pt-BR",
    "pt_BR": "pt-BR",
    "en-us": "en",
    "en_US": "en",
    "en-gb": "en",
    "en_GB": "en",
}


def _discover_locales() -> tuple[str, ...]:
    locales = sorted(path.stem for path in TRANSLATIONS_DIR.glob("*.json"))
    if DEFAULT_LOCALE not in locales:
        locales.insert(0, DEFAULT_LOCALE)
    return tuple(dict.fromkeys(locales))


SUPPORTED_LOCALES = _discover_locales()


def get_supported_locales() -> tuple[str, ...]:
    return SUPPORTED_LOCALES


def normalize_locale(locale: str | None) -> str:
    if not locale:
        return DEFAULT_LOCALE
    cleaned = locale.strip()
    if cleaned in SUPPORTED_LOCALES:
        return cleaned
    lowered = cleaned.lower()
    alias = LOCALE_ALIASES.get(lowered) or LOCALE_ALIASES.get(cleaned)
    if alias in SUPPORTED_LOCALES:
        return alias
    return DEFAULT_LOCALE


@lru_cache(maxsize=16)
def load_translations(locale: str) -> dict[str, Any]:
    normalized = normalize_locale(locale)
    file_path = TRANSLATIONS_DIR / f"{normalized}.json"
    with file_path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"Translation file must contain an object: {file_path}")
    return data


@lru_cache(maxsize=16)
def _default_translations() -> dict[str, Any]:
    return load_translations(DEFAULT_LOCALE)


def get_locale() -> str:
    if request is None:
        return DEFAULT_LOCALE

    requested = request.args.get("lang", "")
    if requested:
        return normalize_locale(requested)

    try:
        best = request.accept_languages.best_match(list(SUPPORTED_LOCALES))
        if best:
            return normalize_locale(best)
    except Exception:
        pass

    return DEFAULT_LOCALE


def _resolve_key(mapping: dict[str, Any], key: str) -> Any:
    if key in mapping:
        return mapping[key]

    current: Any = mapping
    for part in key.split("."):
        if isinstance(current, dict) and part in current:
            current = current[part]
        else:
            return None
    return current


def has_translation_key(locale: str, key: str) -> bool:
    translations = load_translations(locale)
    return _resolve_key(translations, key) is not None


def _same_language_candidates(locale: str) -> list[str]:
    normalized = normalize_locale(locale)
    candidates = [normalized]
    prefix = normalized.split("-")[0]
    for supported in SUPPORTED_LOCALES:
        if supported == normalized:
            continue
        if supported.split("-")[0] == prefix:
            candidates.append(supported)
    return candidates


def translate_key(key: str, locale: str, **kwargs: Any) -> str:
    normalized = normalize_locale(locale)
    translations = load_translations(normalized)

    template = _resolve_key(translations, key)
    if template is None and normalized == DEFAULT_LOCALE:
        template = _resolve_key(_default_translations(), key)
    if template is None:
        template = _resolve_key(translations, "common.missing_translation") or key.replace(".", " ").replace("_", " ").title()

    if not isinstance(template, str):
        return str(template)

    try:
        return template.format(**kwargs)
    except Exception:
        return template


def localize_value(value: Any, locale: str) -> Any:
    normalized = normalize_locale(locale)

    if isinstance(value, dict):
        for candidate in _same_language_candidates(normalized):
            if candidate in value:
                return localize_value(value[candidate], normalized)
        return None

    if isinstance(value, list):
        return [localize_value(item, normalized) for item in value]

    return value
