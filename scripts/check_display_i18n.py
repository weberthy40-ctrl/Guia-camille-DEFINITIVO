from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from utils.data_access import load_camille, load_learning_bundle, load_streamers  # noqa: E402
from utils.i18n import localize_value  # noqa: E402
from utils.integrity import write_json  # noqa: E402

REPORT_FILE = BASE_DIR / "data" / "meta" / "display_i18n_report.json"
LOCALES = ("pt-BR", "en")


def _value_present(value: Any) -> bool:
    if value is None:
        return False
    if isinstance(value, str):
        return value.strip() != ""
    if isinstance(value, list):
        return all(_value_present(item) for item in value)
    return True


def main() -> int:
    camille = load_camille()
    learning = load_learning_bundle()
    streamers = load_streamers()

    checks: dict[str, dict[str, bool]] = {locale: {} for locale in LOCALES}
    leaks: dict[str, list[str]] = {locale: [] for locale in LOCALES}

    for locale in LOCALES:
        guide_values = [
            localize_value(camille.get("summary"), locale),
            localize_value(camille.get("playstyle"), locale),
            localize_value(camille.get("macro_identity"), locale),
            localize_value(camille.get("spikes"), locale),
            [localize_value(item, locale) for item in camille.get("identity", {}).get("tags", [])],
            [localize_value(item, locale) for item in camille.get("most_used_full_build", [])],
            [localize_value(item, locale) for item in camille.get("situational_items", [])],
        ]
        checks[locale]["guide_display_localized"] = all(_value_present(value) for value in guide_values)
        if not checks[locale]["guide_display_localized"]:
            leaks[locale].append("guide_display_localized")

        learning_values = [
            localize_value(learning.get("overview"), locale),
            localize_value(learning.get("streamers_note"), locale),
        ]
        checks[locale]["learning_bundle_localized"] = all(_value_present(value) for value in learning_values)
        if not checks[locale]["learning_bundle_localized"]:
            leaks[locale].append("learning_bundle_localized")

        creator_values = []
        for entry in streamers.get("entries", []):
            creator_values.extend([
                localize_value(entry.get("platform"), locale),
                localize_value(entry.get("language"), locale),
                localize_value(entry.get("focus"), locale),
            ])
        checks[locale]["creator_metadata_localized"] = all(_value_present(value) for value in creator_values)
        if not checks[locale]["creator_metadata_localized"]:
            leaks[locale].append("creator_metadata_localized")

    report = {
        "locales_checked": list(LOCALES),
        "checks": checks,
        "failing_checks": leaks,
        "display_locale_consistent": all(all(results.values()) for results in checks.values()),
        "notes": [
            "This check validates localized display values for guide and learning runtime paths.",
            "It does not render matchup content and does not modify matchup files.",
        ],
    }
    write_json(REPORT_FILE, report)

    if report["display_locale_consistent"]:
        print(f"Display i18n check passed. Report written to {REPORT_FILE}")
        return 0

    print(f"Display i18n inconsistencies found. Report written to {REPORT_FILE}")
    for locale, items in leaks.items():
        for item in items:
            print(f" - {locale}: {item}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
