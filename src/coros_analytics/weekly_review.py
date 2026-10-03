from __future__ import annotations

from collections import defaultdict
from datetime import date, datetime, timedelta
from statistics import mean
from typing import Any

from coros_analytics.models import ActivitySummary, WeeklyBucket, WeeklyReviewResult


def _parse_date(value: str) -> date:
    return datetime.strptime(value[:10], "%Y-%m-%d").date()


def _iso_week_start(day: date) -> date:
    return day - timedelta(days=day.weekday())


def _pace_mean(paces: list[float]) -> float | None:
    return mean(paces) if paces else None


def build_weekly_review(payload: dict[str, Any]) -> WeeklyReviewResult:
    activities = [ActivitySummary.from_dict(item) for item in payload.get("activities", [])]
    if not activities:
        period_start = str(payload.get("period_start", ""))
        period_end = str(payload.get("period_end", ""))
        return WeeklyReviewResult(
            period_start=period_start,
            period_end=period_end,
            total_distance_km=0.0,
            total_duration_h=0.0,
            run_count=0,
            long_run_pct=0.0,
            avg_pace_s_per_km=None,
            weeks=[],
            notes=["No activities in range; verify MCP sport filter and device sync."],
        )

    dates = [_parse_date(a.date) for a in activities]
    period_start = str(payload.get("period_start") or min(dates).isoformat())
    period_end = str(payload.get("period_end") or max(dates).isoformat())

    total_distance_m = sum(a.distance_m for a in activities)
    total_duration_s = sum(a.duration_s for a in activities)
    long_distance_m = sum(a.distance_m for a in activities if a.is_long_run)
    paces = [a.avg_pace_s_per_km for a in activities if a.avg_pace_s_per_km]

    by_week: dict[date, list[ActivitySummary]] = defaultdict(list)
    for activity in activities:
        by_week[_iso_week_start(_parse_date(activity.date))].append(activity)

    weeks: list[WeeklyBucket] = []
    for week_start in sorted(by_week):
        group = by_week[week_start]
        distance_m = sum(a.distance_m for a in group)
        duration_s = sum(a.duration_s for a in group)
        long_m = sum(a.distance_m for a in group if a.is_long_run)
        week_paces = [a.avg_pace_s_per_km for a in group if a.avg_pace_s_per_km]
        weeks.append(
            WeeklyBucket(
                week_start=week_start.isoformat(),
                run_count=len(group),
                distance_km=round(distance_m / 1000.0, 2),
                duration_h=round(duration_s / 3600.0, 2),
                long_run_pct=round((long_m / distance_m) * 100.0, 1) if distance_m else 0.0,
                avg_pace_s_per_km=round(_pace_mean(week_paces), 1) if week_paces else None,
            )
        )

    notes: list[str] = []
    if len(weeks) >= 2:
        delta = weeks[-1].distance_km - weeks[-2].distance_km
        if weeks[-2].distance_km > 0 and delta / weeks[-2].distance_km > 0.3:
            notes.append("Latest week volume rose >30% vs previous week; watch injury risk.")
        if weeks[-2].distance_km > 0 and delta / weeks[-2].distance_km < -0.35:
            notes.append("Latest week volume dropped sharply; confirm intentional recovery or illness.")

    return WeeklyReviewResult(
        period_start=period_start,
        period_end=period_end,
        total_distance_km=round(total_distance_m / 1000.0, 2),
        total_duration_h=round(total_duration_s / 3600.0, 2),
        run_count=len(activities),
        long_run_pct=round((long_distance_m / total_distance_m) * 100.0, 1) if total_distance_m else 0.0,
        avg_pace_s_per_km=round(_pace_mean(paces), 1) if paces else None,
        weeks=weeks,
        notes=notes,
    )
