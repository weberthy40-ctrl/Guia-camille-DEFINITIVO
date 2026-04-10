from .i18n import (
    get_locale,
    get_supported_locales,
    load_translations,
    translate_key,
    localize_value,
    has_translation_key,
)
from .data_access import (
    load_json,
    load_camille,
    load_learning,
    load_learning_bundle,
    load_matchup,
    load_matchups_overview,
    load_roles_index,
    load_external_links,
    load_streamers,
)
from .scoring import calculate_score, calculate_score_from_components, difficulty_from_score, clamp_score

from .assets import (
    get_ddragon_version,
    get_placeholder_relative_path,
    get_local_icon_path,
    has_local_icon,
    slug_to_ddragon_id,
    get_ddragon_icon_url,
    get_champion_icon_payload,
)

from .integrity import (
    LEARNING_FILE_SPECS,
    EXPECTED_PROJECT_FILES,
    read_json_status,
    build_learning_integrity_report,
    build_expected_files_manifest,
    build_merge_readiness_report,
    write_json as write_integrity_json,
)

from .terms import localize_term, matchup_field_label
