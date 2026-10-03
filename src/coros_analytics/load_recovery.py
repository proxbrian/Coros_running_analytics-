from __future__ import annotations

from typing import Any

from coros_analytics.models import LoadRecoveryInput, LoadRecoveryResult


def assess_load_recovery(payload: dict[str, Any]) -> LoadRecoveryResult:
    data = LoadRecoveryInput.from_dict(payload)
    ratio = data.load_ratio
    if ratio is None:
        if data.chronic_load <= 0:
            ratio = 1.0
        else:
            ratio = data.acute_load / data.chronic_load

    risk_flags: list[str] = []
    rationale: list[str] = [f"Load ratio (acute/chronic) ≈ {ratio:.2f}."]

    if ratio >= 1.5:
        risk_flags.append("high_acute_load")
        rationale.append("Acute load is substantially above chronic load.")
    elif ratio >= 1.3:
        risk_flags.append("elevated_acute_load")
        rationale.append("Acute load is elevated relative to chronic load.")

    if data.recovery_pct is not None:
        rationale.append(f"Recovery status ≈ {data.recovery_pct:.0f}%.")
        if data.recovery_pct < 40:
            risk_flags.append("low_recovery")
        elif data.recovery_pct < 60:
            risk_flags.append("moderate_recovery")

    if data.sleep_score_avg is not None:
        rationale.append(f"Average sleep score ≈ {data.sleep_score_avg:.0f}.")
        if data.sleep_score_avg < 65:
            risk_flags.append("poor_sleep")

    if data.hrv_status:
        status = data.hrv_status.lower()
        rationale.append(f"HRV status: {data.hrv_status}.")
        if status in {"low", "unbalanced", "poor"}:
            risk_flags.append("hrv_concern")

    if data.resting_hr_delta is not None:
        rationale.append(f"Resting HR delta vs baseline ≈ {data.resting_hr_delta:+.1f} bpm.")
        if data.resting_hr_delta >= 5:
            risk_flags.append("elevated_rhr")

    recommendation = _recommend(ratio, risk_flags)
    return LoadRecoveryResult(
        recommendation=recommendation,
        load_ratio=round(ratio, 2),
        risk_flags=risk_flags,
        rationale=rationale,
    )


def _recommend(ratio: float, risk_flags: list[str]) -> str:
    flags = set(risk_flags)
    hard_flags = {"low_recovery", "poor_sleep", "hrv_concern", "elevated_rhr", "high_acute_load"}
    if flags & hard_flags or ratio >= 1.5:
        if "low_recovery" in flags or "hrv_concern" in flags:
            return "rest"
        return "easy"
    if "elevated_acute_load" in flags or "moderate_recovery" in flags:
        return "easy"
    if ratio < 0.8:
        return "normal"
    return "quality"
