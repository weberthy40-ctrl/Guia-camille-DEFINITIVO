from __future__ import annotations

from typing import Mapping

SCORE_WEIGHTS = {
    "lane_phase_pressure": 0.40,
    "gold_diff_15": 0.25,
    "kill_threat": 0.20,
    "matchup_winrate_pressure": 0.15,
}
SCORE_MIN = 1.0
SCORE_MAX = 10.0



def clamp_score(score: float) -> float:
    return round(max(SCORE_MIN, min(SCORE_MAX, float(score))), 1)



def calculate_score(
    lane_phase_pressure: float,
    gold_diff_15: float,
    kill_threat: float,
    matchup_winrate_pressure: float,
) -> float:
    score = (
        float(lane_phase_pressure) * SCORE_WEIGHTS["lane_phase_pressure"]
        + float(gold_diff_15) * SCORE_WEIGHTS["gold_diff_15"]
        + float(kill_threat) * SCORE_WEIGHTS["kill_threat"]
        + float(matchup_winrate_pressure) * SCORE_WEIGHTS["matchup_winrate_pressure"]
    )
    return clamp_score(score)



def calculate_score_from_components(scoring_block: Mapping[str, float]) -> float:
    return calculate_score(
        scoring_block.get("lane_phase_pressure", 1.0),
        scoring_block.get("gold_diff_15", 1.0),
        scoring_block.get("kill_threat", 1.0),
        scoring_block.get("matchup_winrate_pressure", 1.0),
    )



def difficulty_from_score(score: float) -> str:
    normalized = clamp_score(score)
    if normalized >= 9.0:
        return "suggest_ban"
    if normalized >= 7.0:
        return "hard"
    if normalized >= 4.5:
        return "medium"
    return "easy"
