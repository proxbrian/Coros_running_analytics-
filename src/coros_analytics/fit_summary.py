from __future__ import annotations

from pathlib import Path
from statistics import mean
from typing import Any


def summarize_fit(fit_path: str | Path) -> dict[str, Any]:
    """Summarize a FIT file. Falls back to a clear error if fitparse cannot parse."""
    path = Path(fit_path)
    if not path.exists():
        raise FileNotFoundError(f"FIT file not found: {path}")

    try:
        from fitparse import FitFile
    except ImportError as exc:  # pragma: no cover
        raise RuntimeError("fitparse is required: pip install fitparse") from exc

    fit = FitFile(str(path))
    records: list[dict[str, Any]] = []
    session: dict[str, Any] = {}

    for message in fit.get_messages():
        name = message.name
        fields = {field.name: field.value for field in message if field.value is not None}
        if name == "record":
            records.append(fields)
        elif name == "session" and not session:
            session = fields

    speeds = [float(r["speed"]) for r in records if r.get("speed") not in (None, 0)]
    hrs = [float(r["heart_rate"]) for r in records if r.get("heart_rate") is not None]
    alts = [float(r["altitude"]) for r in records if r.get("altitude") is not None]
    cadences = [float(r["cadence"]) for r in records if r.get("cadence") is not None]

    distance_m = _first_number(session, ("total_distance",)) or _last_number(records, "distance")
    elapsed_s = _first_number(session, ("total_elapsed_time", "total_timer_time"))
    avg_hr = _first_number(session, ("avg_heart_rate",)) or (mean(hrs) if hrs else None)
    max_hr = _first_number(session, ("max_heart_rate",)) or (max(hrs) if hrs else None)
    elev_gain = _first_number(session, ("total_ascent",))
    if elev_gain is None and len(alts) >= 2:
        elev_gain = sum(max(0.0, alts[i] - alts[i - 1]) for i in range(1, len(alts)))

    avg_speed = _first_number(session, ("avg_speed",)) or (mean(speeds) if speeds else None)
    pace = (1000.0 / avg_speed) if avg_speed and avg_speed > 0 else None

    return {
        "file": str(path),
        "record_count": len(records),
        "distance_km": round(distance_m / 1000.0, 3) if distance_m is not None else None,
        "elapsed_min": round(elapsed_s / 60.0, 2) if elapsed_s is not None else None,
        "avg_pace_s_per_km": round(pace, 1) if pace is not None else None,
        "avg_hr": round(avg_hr, 1) if avg_hr is not None else None,
        "max_hr": round(max_hr, 1) if max_hr is not None else None,
        "elevation_gain_m": round(elev_gain, 1) if elev_gain is not None else None,
        "avg_cadence": round(mean(cadences), 1) if cadences else None,
        "notes": _notes(hrs, paces_available=pace is not None),
    }


def _first_number(data: dict[str, Any], keys: tuple[str, ...]) -> float | None:
    for key in keys:
        value = data.get(key)
        if value is not None:
            return float(value)
    return None


def _last_number(records: list[dict[str, Any]], key: str) -> float | None:
    for record in reversed(records):
        if record.get(key) is not None:
            return float(record[key])
    return None


def _notes(hrs: list[float], *, paces_available: bool) -> list[str]:
    notes: list[str] = []
    if not paces_available:
        notes.append("No usable speed/pace in FIT records.")
    if hrs:
        span = max(hrs) - min(hrs)
        if span >= 40:
            notes.append("Wide heart-rate range; inspect intervals or hills separately.")
    else:
        notes.append("No heart-rate samples in FIT records.")
    return notes
