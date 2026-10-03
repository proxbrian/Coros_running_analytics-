from coros_analytics.race_readiness import assess_race_readiness


def test_half_nearly_ready():
    result = assess_race_readiness(
        {
            "target": "half",
            "weeks_to_race": 6,
            "predicted_seconds": 6300,
            "goal_seconds": 6600,
            "weekly_distance_km": 48,
            "peak_weekly_distance_km": 62,
            "long_run_km": 20,
            "load_ratio": 1.05,
        }
    )
    assert result.score >= 65
    assert result.band in {"ready", "nearly_ready"}


def test_underprepared_marathon():
    result = assess_race_readiness(
        {
            "target": "marathon",
            "weeks_to_race": 4,
            "weekly_distance_km": 25,
            "peak_weekly_distance_km": 30,
            "long_run_km": 16,
            "load_ratio": 1.6,
        }
    )
    assert result.score < 45
    assert result.band == "underprepared"
    assert result.gaps
