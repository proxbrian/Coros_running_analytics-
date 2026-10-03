from __future__ import annotations

from typing import Any

from coros_analytics.models import RaceReadinessInput, RaceReadinessResult

# Rough volume heuristics (km/week and long-run km) for recreational readiness.
_TARGET_BENCHMARKS: dict[str, dict[str, float]] = {
    "5k": {"weekly": 25.0, "peak": 35.0, "long": 10.0},
    "10k": {"weekly": 35.0, "peak": 45.0, "long": 14.0},
    "half": {"weekly": 45.0, "peak": 60.0, "long": 18.0},
    "marathon": {"weekly": 60.0, "peak": 80.0, "long": 30.0},
}


def assess_race_readiness(payload: dict[str, Any]) -> RaceReadinessResult:
    data = RaceReadinessInput.from_dict(payload)
    if data.target not in _TARGET_BENCHMARKS:
        raise ValueError(f"Unsupported target: {data.target}. Use 5k|10k|half|marathon.")

    bench = _TARGET_BENCHMARKS[data.target]
    score = 50
    gaps: list[str] = []
    strengths: list[str] = []
    notes: list[str] = []

    # Volume
    if data.weekly_distance_km >= bench["weekly"]:
        score += 12
        strengths.append("Recent weekly volume meets baseline for the distance.")
    else:
        score -= 10
        gaps.append(
            f"Weekly volume {data.weekly_distance_km:.1f} km is below ~{bench['weekly']:.0f} km baseline."
        )

    if data.peak_weekly_distance_km >= bench["peak"]:
        score += 10
        strengths.append("Peak week volume looks adequate.")
    else:
        score -= 8
        gaps.append(
            f"Peak week {data.peak_weekly_distance_km:.1f} km is below ~{bench['peak']:.0f} km."
        )

    if data.long_run_km >= bench["long"]:
        score += 12
        strengths.append("Longest recent run supports the race distance.")
    else:
        score -= 12
        gaps.append(f"Longest run {data.long_run_km:.1f} km is below ~{bench['long']:.0f} km.")

    # Goal vs prediction
    if data.predicted_seconds and data.goal_seconds:
        ratio = data.goal_seconds / data.predicted_seconds
        if ratio >= 1.05:
            score += 8
            strengths.append("Goal pace is conservative vs COROS prediction.")
        elif ratio >= 0.97:
            score += 3
            notes.append("Goal is close to COROS prediction; execution risk is moderate.")
        else:
            score -= 10
            gaps.append("Goal is meaningfully faster than COROS prediction.")

    # Timing / taper
    if data.weeks_to_race <= 2:
        notes.append("Inside taper window: prioritize freshness over new fitness.")
        if data.load_ratio and data.load_ratio > 1.2:
            score -= 8
            gaps.append("Load still high this close to race; reduce intensity.")
        else:
            score += 5
    elif data.weeks_to_race >= 10 and data.weekly_distance_km < bench["weekly"] * 0.7:
        notes.append("Plenty of time remains to build volume gradually.")

    if data.load_ratio is not None:
        if 0.8 <= data.load_ratio <= 1.3:
            score += 5
            strengths.append("Training load ratio is in a productive band.")
        elif data.load_ratio > 1.5:
            score -= 8
            gaps.append("Acute load spike may compromise readiness.")

    score = max(0, min(100, score))
    band = _band(score)
    return RaceReadinessResult(
        target=data.target,
        score=score,
        band=band,
        gaps=gaps,
        strengths=strengths,
        notes=notes,
    )


def _band(score: int) -> str:
    if score >= 80:
        return "ready"
    if score >= 65:
        return "nearly_ready"
    if score >= 45:
        return "developing"
    return "underprepared"
