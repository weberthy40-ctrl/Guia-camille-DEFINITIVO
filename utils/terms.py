from __future__ import annotations

from typing import Any

from .i18n import normalize_locale

TERM_MAP = {
    # items
    'Trinity Force': {'pt-BR': 'Força da Trindade', 'en': 'Trinity Force'},
    'Force of Trinity': {'pt-BR': 'Força da Trindade', 'en': 'Trinity Force'},
    'Ravenous Hydra': {'pt-BR': 'Hidra Raivosa', 'en': 'Ravenous Hydra'},
    'Titanic Hydra': {'pt-BR': 'Hidra Titânica', 'en': 'Titanic Hydra'},
    'Plated Steelcaps': {'pt-BR': 'Passos de Aço Platinados', 'en': 'Plated Steelcaps'},
    "Mercury's Treads": {'pt-BR': 'Passos de Mercúrio', 'en': "Mercury's Treads"},
    "Boots of Swiftness": {'pt-BR': 'Botas da Rapidez', 'en': 'Boots of Swiftness'},
    "Death's Dance": {'pt-BR': 'Dança da Morte', 'en': "Death's Dance"},
    "Sterak's Gage": {'pt-BR': 'Gage de Sterak', 'en': "Sterak's Gage"},
    'Guardian Angel': {'pt-BR': 'Anjo Guardião', 'en': 'Guardian Angel'},
    'Maw of Malmortius': {'pt-BR': 'Mandíbula de Malmortius', 'en': 'Maw of Malmortius'},
    'Sundered Sky': {'pt-BR': 'Céu Dividido', 'en': 'Sundered Sky'},
    'Spear of Shojin': {'pt-BR': 'Lança de Shojin', 'en': 'Spear of Shojin'},
    'Frozen Heart': {'pt-BR': 'Coração Congelado', 'en': 'Frozen Heart'},
    "Randuin's Omen": {'pt-BR': 'Presságio de Randuin', 'en': "Randuin's Omen"},
    'Chempunk Chainsword': {'pt-BR': 'Espada-serra Quimtec', 'en': 'Chempunk Chainsword'},
    'Executioner\'s Calling': {'pt-BR': 'Chamado do Carrasco', 'en': "Executioner's Calling"},
    'Bramble Vest': {'pt-BR': 'Colete Espinhoso', 'en': 'Bramble Vest'},
    'Hexdrinker': {'pt-BR': 'Bebedor de Hexdrinque', 'en': 'Hexdrinker'},
    'Cloth Armor': {'pt-BR': 'Armadura de Pano', 'en': 'Cloth Armor'},
    "Doran's Shield": {'pt-BR': 'Escudo de Doran', 'en': "Doran's Shield"},
    "Doran's Blade": {'pt-BR': 'Lâmina de Doran', 'en': "Doran's Blade"},
    'Long Sword': {'pt-BR': 'Espada Longa', 'en': 'Long Sword'},
    'Cull': {'pt-BR': 'Foice do Ceifador', 'en': 'Cull'},
    'Corrupting Potion': {'pt-BR': 'Poção de Corrupção', 'en': 'Corrupting Potion'},
    'Situational boots': {'pt-BR': 'Botas situacionais', 'en': 'Situational boots'},
    # runes
    'Grasp': {'pt-BR': 'Aperto dos Mortos-Vivos', 'en': 'Grasp of the Undying'},
    'Grasp of the Undying': {'pt-BR': 'Aperto dos Mortos-Vivos', 'en': 'Grasp of the Undying'},
    'Press the Attack': {'pt-BR': 'Pressione o Ataque', 'en': 'Press the Attack'},
    'Conqueror': {'pt-BR': 'Conquistador', 'en': 'Conqueror'},
    'Resolve': {'pt-BR': 'Determinação', 'en': 'Resolve'},
    'Precision': {'pt-BR': 'Precisão', 'en': 'Precision'},
    'Inspiration': {'pt-BR': 'Inspiração', 'en': 'Inspiration'},
    'Shield Bash': {'pt-BR': 'Golpe de Escudo', 'en': 'Shield Bash'},
    'Demolish': {'pt-BR': 'Demolir', 'en': 'Demolish'},
    'Bone Plating': {'pt-BR': 'Osso Revestido', 'en': 'Bone Plating'},
    'Second Wind': {'pt-BR': 'Ventos Revigorantes', 'en': 'Second Wind'},
    'Overgrowth': {'pt-BR': 'Crescimento Excessivo', 'en': 'Overgrowth'},
    'Unflinching': {'pt-BR': 'Inabalável', 'en': 'Unflinching'},
    'Triumph': {'pt-BR': 'Triunfo', 'en': 'Triumph'},
    'Presence of Mind': {'pt-BR': 'Presença de Espírito', 'en': 'Presence of Mind'},
    'Legend: Alacrity': {'pt-BR': 'Lenda: Espontaneidade', 'en': 'Legend: Alacrity'},
    'Legend: Haste': {'pt-BR': 'Lenda: Aceleração', 'en': 'Legend: Haste'},
    'Last Stand': {'pt-BR': 'Até a Morte', 'en': 'Last Stand'},
    'Cut Down': {'pt-BR': 'Dilacerar', 'en': 'Cut Down'},
    'Biscuit Delivery': {'pt-BR': 'Entrega de Biscoitos', 'en': 'Biscuit Delivery'},
    'Magical Footwear': {'pt-BR': 'Calçados Mágicos', 'en': 'Magical Footwear'},
    'Cosmic Insight': {'pt-BR': 'Perspicácia Cósmica', 'en': 'Cosmic Insight'},
    'Jack of All Trades': {'pt-BR': 'Jack of All Trades', 'en': 'Jack of All Trades'},
    'Attack Speed': {'pt-BR': 'Velocidade de Ataque', 'en': 'Attack Speed'},
    'Adaptive Force': {'pt-BR': 'Força Adaptativa', 'en': 'Adaptive Force'},
    'Health Scaling': {'pt-BR': 'Vida Escalável', 'en': 'Health Scaling'},
    'Armor': {'pt-BR': 'Armadura', 'en': 'Armor'},
    'Magic Resist': {'pt-BR': 'Resistência Mágica', 'en': 'Magic Resist'},
    # misc interface values
    'high': {'pt-BR': 'alta', 'en': 'high'},
    'medium': {'pt-BR': 'média', 'en': 'medium'},
    'low': {'pt-BR': 'baixa', 'en': 'low'},
    'top': {'pt-BR': 'topo', 'en': 'top'},
}

PHRASE_MAP = {
    'Second Wind / Grasp page': {
        'pt-BR': 'Ventos Revigorantes / página de Aperto dos Mortos-Vivos',
        'en': 'Second Wind / Grasp page',
    },
    'Early Cloth Armor if lane is unstable': {
        'pt-BR': 'Armadura de Pano cedo se a lane estiver instável',
        'en': 'Early Cloth Armor if lane is unstable',
    },
    'Bramble Vest if healing becomes unmanageable': {
        'pt-BR': 'Colete Espinhoso se a cura ficar impossível de controlar',
        'en': 'Bramble Vest if healing becomes unmanageable',
    },
    'Executioner\'s Calling if anti-heal is urgent': {
        'pt-BR': 'Chamado do Carrasco se anti-cura for urgente',
        'en': "Executioner's Calling if anti-heal is urgent",
    },
    'Early Hexdrinker if burst AP decides the lane': {
        'pt-BR': 'Bebedor de Hexdrinque cedo se burst AP decidir a lane',
        'en': 'Early Hexdrinker if burst AP decides the lane',
    },
}

FIELD_LABELS = {
    'quick_summary': {'pt-BR': 'Resumo rápido', 'en': 'Quick summary'},
    'enemy_identity': {'pt-BR': 'Identidade do inimigo', 'en': 'Enemy identity'},
    'matchup_type': {'pt-BR': 'Tipo de matchup', 'en': 'Matchup type'},
    'threat_level': {'pt-BR': 'Nível de ameaça', 'en': 'Threat level'},
    'confidence': {'pt-BR': 'Confiança', 'en': 'Confidence'},
    'punish_window': {'pt-BR': 'Janela de punição', 'en': 'Punish window'},
    'trade_timing': {'pt-BR': 'Timing de troca', 'en': 'Trade timing'},
    'safe_play': {'pt-BR': 'Postura segura', 'en': 'Safe play'},
    'all_in_condition': {'pt-BR': 'Condição de all-in', 'en': 'All-in condition'},
    'early_plan': {'pt-BR': 'Plano inicial', 'en': 'Early plan'},
    'level_1_3': {'pt-BR': 'Níveis 1-3', 'en': 'Levels 1-3'},
    'level_4_5': {'pt-BR': 'Níveis 4-5', 'en': 'Levels 4-5'},
    'level_6': {'pt-BR': 'Nível 6', 'en': 'Level 6'},
    'post_6': {'pt-BR': 'Pós-6', 'en': 'Post-6'},
    'most_used': {'pt-BR': 'Página principal', 'en': 'Primary page'},
    'highest_winrate': {'pt-BR': 'Leitura de maior rendimento', 'en': 'Highest value read'},
    'situational': {'pt-BR': 'Página situacional', 'en': 'Situational page'},
    'when_to_use_each': {'pt-BR': 'Quando usar cada uma', 'en': 'When to use each'},
    'matchup_specific_reason': {'pt-BR': 'Por que nesta lane', 'en': 'Why in this lane'},
    'start_items': {'pt-BR': 'Início', 'en': 'Start items'},
    'core_items': {'pt-BR': 'Núcleo', 'en': 'Core items'},
    'full_build': {'pt-BR': 'Build completa', 'en': 'Full build'},
    'situational_items': {'pt-BR': 'Itens situacionais', 'en': 'Situational items'},
    'decision_build': {'pt-BR': 'Decisão de build', 'en': 'Build decision'},
    'behind': {'pt-BR': 'Se estiver atrás', 'en': 'When behind'},
    'ahead': {'pt-BR': 'Se estiver na frente', 'en': 'When ahead'},
    'vs_ap': {'pt-BR': 'Contra muito AP', 'en': 'Into heavy AP'},
    'vs_tank': {'pt-BR': 'Contra front line/tanque', 'en': 'Into tanks/frontline'},
    'lane_phase_pressure': {'pt-BR': 'Pressão de lane', 'en': 'Lane pressure'},
    'gold_diff_15': {'pt-BR': 'Pressão econômica @15', 'en': 'Gold pressure @15'},
    'kill_threat': {'pt-BR': 'Ameaça de abate', 'en': 'Kill threat'},
    'matchup_winrate_pressure': {'pt-BR': 'Pressão estatística', 'en': 'Stat pressure'},
    'formula_version': {'pt-BR': 'Versão da fórmula', 'en': 'Formula version'},
}


def localize_term(value: Any, locale: str) -> Any:
    locale = normalize_locale(locale)
    if isinstance(value, list):
        return [localize_term(item, locale) for item in value]
    if isinstance(value, dict):
        return {k: localize_term(v, locale) for k, v in value.items()}
    if not isinstance(value, str):
        return value
    if value in PHRASE_MAP:
        return PHRASE_MAP[value].get(locale, value)
    if value in TERM_MAP:
        return TERM_MAP[value].get(locale, value)
    # translate slash-separated rune/item pairs
    if ' / ' in value:
        return ' / '.join(str(localize_term(part, locale)) for part in value.split(' / '))
    return value


def matchup_field_label(key: str, locale: str) -> str:
    locale = normalize_locale(locale)
    if key in FIELD_LABELS:
        return FIELD_LABELS[key].get(locale, key.replace('_', ' ').title())
    return key.replace('_', ' ').replace('15', '@15').title()
