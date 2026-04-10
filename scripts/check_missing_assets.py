from __future__ import annotations

import json
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from utils.assets import (  # noqa: E402
    get_champion_icon_payload,
    get_ddragon_icon_url,
    get_ddragon_version,
    get_local_icon_path,
    get_placeholder_relative_path,
)

INDEX_FILE = BASE_DIR / "data" / "meta" / "champions_index.json"
CAMILLE_DIR = BASE_DIR / "static" / "img" / "camille"
REPORT_FILE = BASE_DIR / "data" / "meta" / "assets_report.json"


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)



def write_json(path: Path, payload) -> None:
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)
        handle.write("\n")



def main() -> None:
    champions = load_json(INDEX_FILE)

    missing_local_icons = []
    unresolved_icons = []
    resolved_via_external = []
    external_url_samples = {}
    existing_local_icons = 0

    for entry in champions:
        slug = entry["slug"]
        payload = get_champion_icon_payload(slug)
        if get_local_icon_path(slug).exists():
            existing_local_icons += 1
        else:
            missing_local_icons.append(slug)

        external_url = get_ddragon_icon_url(slug)
        if external_url:
            resolved_via_external.append(slug)
            if len(external_url_samples) < 12:
                external_url_samples[slug] = external_url
        elif payload["resolved_by"] == "placeholder":
            unresolved_icons.append(slug)

    placeholder_path = BASE_DIR / "static" / get_placeholder_relative_path()
    camille_assets = {
        "available": sorted(path.name for path in CAMILLE_DIR.glob("*") if path.is_file()),
        "missing_expected": [],
    }
    for expected in ["camille-hero.svg"]:
        if not (CAMILLE_DIR / expected).exists():
            camille_assets["missing_expected"].append(expected)

    report = {
        "champion_icon_total": len(champions),
        "champion_icon_present": existing_local_icons,
        "champion_icon_missing": missing_local_icons,
        "champion_icon_resolvable": len(champions) - len(unresolved_icons),
        "champion_icon_unresolved": unresolved_icons,
        "champion_icon_external_resolvable": len(resolved_via_external),
        "external_provider": "Riot Data Dragon",
        "external_provider_version": get_ddragon_version(),
        "external_url_samples": external_url_samples,
        "placeholder_present": placeholder_path.exists(),
        "camille_assets": camille_assets,
    }
    write_json(REPORT_FILE, report)

    print(f"Asset report written to {REPORT_FILE}")
    print(f"Local champion icons present: {existing_local_icons}/{len(champions)}")
    print(f"Champion icons resolvable via provider or local assets: {report['champion_icon_resolvable']}/{len(champions)}")
    if missing_local_icons:
        preview = ", ".join(missing_local_icons[:15])
        print(f"Local icons still missing sample: {preview}")
    if unresolved_icons:
        unresolved_preview = ", ".join(unresolved_icons[:15])
        print(f"Unresolved icons sample: {unresolved_preview}")
    else:
        print("No champion icon slugs are unresolved.")


if __name__ == "__main__":
    main()
