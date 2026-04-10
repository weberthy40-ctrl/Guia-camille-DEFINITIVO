from __future__ import annotations

import os
import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = BASE_DIR / "static"
CHAMPION_ICON_DIR = STATIC_DIR / "img" / "champions" / "icons"
PLACEHOLDER_RELATIVE_PATH = "img/champions/icons/placeholder.svg"
DEFAULT_DDRAGON_VERSION = os.getenv("LOL_DDRAGON_VERSION", "16.7.1")

SPECIAL_DDRAGON_IDS = {
    "jarvan-iv": "JarvanIV",
    "kaisa": "KaiSa",
    "ksante": "KSante",
    "kogmaw": "KogMaw",
    "nunu-and-willump": "Nunu",
    "reksai": "RekSai",
    "renata-glasc": "Renata",
    "wukong": "MonkeyKing",
}


def get_ddragon_version() -> str:
    return DEFAULT_DDRAGON_VERSION



def get_placeholder_relative_path() -> str:
    return PLACEHOLDER_RELATIVE_PATH



def get_local_icon_path(slug: str | None) -> Path:
    safe_slug = (slug or "").strip().lower()
    return CHAMPION_ICON_DIR / f"{safe_slug}.png"



def has_local_icon(slug: str | None) -> bool:
    return get_local_icon_path(slug).exists()



def slug_to_ddragon_id(slug: str | None) -> str | None:
    cleaned = (slug or "").strip().lower()
    if not cleaned:
        return None
    if cleaned in SPECIAL_DDRAGON_IDS:
        return SPECIAL_DDRAGON_IDS[cleaned]

    parts = [part for part in re.split(r"[-_\s]+", cleaned) if part]
    if not parts:
        return None
    return "".join(part.capitalize() for part in parts)



def get_ddragon_icon_url(slug: str | None, version: str | None = None) -> str | None:
    champion_id = slug_to_ddragon_id(slug)
    if not champion_id:
        return None
    asset_version = (version or get_ddragon_version()).strip() or get_ddragon_version()
    return f"https://ddragon.leagueoflegends.com/cdn/{asset_version}/img/champion/{champion_id}.png"



def get_champion_icon_payload(slug: str | None, version: str | None = None) -> dict[str, str | bool | None]:
    fallback = get_placeholder_relative_path()

    if has_local_icon(slug):
        return {
            "src": f"img/champions/icons/{(slug or '').strip().lower()}.png",
            "fallback": fallback,
            "resolved_by": "local",
            "version": version or get_ddragon_version(),
            "local_exists": True,
        }

    external_url = get_ddragon_icon_url(slug, version=version)
    if external_url:
        return {
            "src": external_url,
            "fallback": fallback,
            "resolved_by": "ddragon",
            "version": version or get_ddragon_version(),
            "local_exists": False,
        }

    return {
        "src": fallback,
        "fallback": fallback,
        "resolved_by": "placeholder",
        "version": version or get_ddragon_version(),
        "local_exists": False,
    }
