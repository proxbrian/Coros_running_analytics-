from coros_analytics.load_recovery import assess_load_recovery


def test_elevated_load_suggests_easy():
    result = assess_load_recovery(
        {
            "acute_load": 420,
            "chronic_load": 310,
            "load_ratio": 1.35,
            "recovery_pct": 52,
            "sleep_score_avg": 72,
            "hrv_status": "balanced",
            "resting_hr_delta": 2,
        }
    )
    assert result.recommendation == "easy"
    assert "elevated_acute_load" in result.risk_flags


def test_low_recovery_suggests_rest():
    result = assess_load_recovery(
        {
            "acute_load": 200,
            "chronic_load": 250,
            "recovery_pct": 30,
            "sleep_score_avg": 60,
            "hrv_status": "low",
            "resting_hr_delta": 6,
        }
    )
    assert result.recommendation == "rest"
