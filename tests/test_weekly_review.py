from coros_analytics.weekly_review import build_weekly_review


def test_weekly_review_totals_and_long_run_pct():
    payload = {
        "period_start": "2026-09-01",
        "period_end": "2026-09-14",
        "activities": [
            {
                "id": "1",
                "date": "2026-09-02",
                "distance_m": 10000,
                "duration_s": 3000,
                "avg_pace_s_per_km": 300,
                "is_long_run": False,
            },
            {
                "id": "2",
                "date": "2026-09-07",
                "distance_m": 20000,
                "duration_s": 7000,
                "avg_pace_s_per_km": 350,
                "is_long_run": True,
            },
            {
                "id": "3",
                "date": "2026-09-09",
                "distance_m": 10000,
                "duration_s": 3100,
                "avg_pace_s_per_km": 310,
                "is_long_run": False,
            },
        ],
    }
    result = build_weekly_review(payload)
    assert result.run_count == 3
    assert result.total_distance_km == 40.0
    assert result.long_run_pct == 50.0
    assert len(result.weeks) == 2


def test_weekly_review_empty():
    result = build_weekly_review({"period_start": "2026-01-01", "period_end": "2026-01-07", "activities": []})
    assert result.run_count == 0
    assert result.notes
