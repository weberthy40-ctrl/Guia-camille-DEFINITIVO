from __future__ import annotations

import json
import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
TRANSLATIONS_DIR = BASE_DIR / "translations"
TEMPLATE_DIR = BASE_DIR / "templates"
SUPPORTED = ("pt-BR", "en")
KEY_PATTERN = re.compile(r"t\(\s*['\"]([^'\"]+)['\"]")
RAW_TEXT_PATTERN = re.compile(r">([^<{]+)<")


def load_translation(locale: str) -> dict[str, str]:
    path = TRANSLATIONS_DIR / f"{locale}.json"
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"Translation file must contain an object: {path}")
    return data


def template_keys() -> set[str]:
    keys: set[str] = set()
    for path in TEMPLATE_DIR.rglob("*.html"):
        content = path.read_text(encoding="utf-8")
        for key in KEY_PATTERN.findall(content):
            if key.endswith("_"):
                continue
            keys.add(key)
    return keys


def hardcoded_template_text() -> dict[str, list[str]]:
    findings: dict[str, list[str]] = {}
    for path in TEMPLATE_DIR.rglob("*.html"):
        content = path.read_text(encoding="utf-8")
        items: list[str] = []
        for match in RAW_TEXT_PATTERN.findall(content):
            cleaned = " ".join(match.split())
            if not cleaned:
                continue
            if "{{" in cleaned or "{%" in cleaned:
                continue
            if re.search(r"[A-Za-zÀ-ÿ]", cleaned):
                items.append(cleaned)
        if items:
            findings[str(path.relative_to(BASE_DIR))] = sorted(set(items))
    return findings


def main() -> int:
    translations = {locale: load_translation(locale) for locale in SUPPORTED}
    all_keys = set().union(*(translations[locale].keys() for locale in SUPPORTED))
    template_key_set = template_keys()

    missing_by_locale = {
        locale: sorted((all_keys | template_key_set) - set(translations[locale].keys()))
        for locale in SUPPORTED
    }

    report = {
        "supported_locales": list(SUPPORTED),
        "template_translation_keys": sorted(template_key_set),
        "missing_by_locale": missing_by_locale,
        "hardcoded_template_text": hardcoded_template_text(),
    }

    report_path = BASE_DIR / "data" / "meta" / "i18n_report.json"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    if any(missing_by_locale.values()):
        print("Missing translation keys detected. See data/meta/i18n_report.json")
        return 1

    print("I18n check passed. Report written to data/meta/i18n_report.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
