from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(slots=True)
class ActivitySummary:
    id: str
    date: str
    sport: str
    distance_m: float
    duration_s: float
    avg_pace_s_per_km: float | None = None
    avg_hr: float | None = None
    elevation_gain_m: float | None = None
    is_long_run: bool = False

    @classmethod
    def from_dict(cls, raw: dict[str, Any]) -> ActivitySummary:
        return cls(
            id=str(raw["id"]),
            date=str(raw["date"]),
            sport=str(raw.get("sport", "run")),
            distance_m=float(raw["distance_m"]),
            duration_s=float(raw["duration_s"]),
            avg_pace_s_per_km=_optional_float(raw.get("avg_pace_s_per_km")),
            avg_hr=_optional_float(raw.get("avg_hr")),
            elevation_gain_m=_optional_float(raw.get("elevation_gain_m")),
            is_long_run=bool(raw.get("is_long_run", False)),
        )


@dataclass(slots=True)
class WeeklyBucket:
    week_start: str
    run_count: int
    distance_km: float
    duration_h: float
    long_run_pct: float
    avg_pace_s_per_km: float | None


@dataclass(slots=True)
class WeeklyReviewResult:
    period_start: str
    period_end: str
    total_distance_km: float
    total_duration_h: float
    run_count: int
    long_run_pct: float
    avg_pace_s_per_km: float | None
    weeks: list[WeeklyBucket] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class LoadRecoveryInput:
    acute_load: float
    chronic_load: float
    load_ratio: float | None
    recovery_pct: float | None
    sleep_score_avg: float | None
    hrv_status: str | None
    resting_hr_delta: float | None

    @classmethod
    def from_dict(cls, raw: dict[str, Any]) -> LoadRecoveryInput:
        return cls(
            acute_load=float(raw["acute_load"]),
            chronic_load=float(raw["chronic_load"]),
            load_ratio=_optional_float(raw.get("load_ratio")),
            recovery_pct=_optional_float(raw.get("recovery_pct")),
            sleep_score_avg=_optional_float(raw.get("sleep_score_avg")),
            hrv_status=(str(raw["hrv_status"]) if raw.get("hrv_status") is not None else None),
            resting_hr_delta=_optional_float(raw.get("resting_hr_delta")),
        )


@dataclass(slots=True)
class LoadRecoveryResult:
    recommendation: str
    load_ratio: float
    risk_flags: list[str]
    rationale: list[str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class RaceReadinessInput:
    target: str
    weeks_to_race: int
    predicted_seconds: float | None
    goal_seconds: float | None
    weekly_distance_km: float
    peak_weekly_distance_km: float
    long_run_km: float
    load_ratio: float | None

    @classmethod
    def from_dict(cls, raw: dict[str, Any]) -> RaceReadinessInput:
        return cls(
            target=str(raw["target"]).lower(),
            weeks_to_race=int(raw["weeks_to_race"]),
            predicted_seconds=_optional_float(raw.get("predicted_seconds")),
            goal_seconds=_optional_float(raw.get("goal_seconds")),
            weekly_distance_km=float(raw["weekly_distance_km"]),
            peak_weekly_distance_km=float(raw["peak_weekly_distance_km"]),
            long_run_km=float(raw["long_run_km"]),
            load_ratio=_optional_float(raw.get("load_ratio")),
        )


@dataclass(slots=True)
class RaceReadinessResult:
    target: str
    score: int
    band: str
    gaps: list[str]
    strengths: list[str]
    notes: list[str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _optional_float(value: Any) -> float | None:
    if value is None or value == "":
        return None
    return float(value)
