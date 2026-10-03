import json
from pathlib import Path

from coros_analytics.cli import main

ROOT = Path(__file__).resolve().parents[1]
SAMPLE = ROOT / "sample_data"


def test_cli_weekly_review(capsys):
    code = main(["weekly-review", "--input", str(SAMPLE / "activities_4w.json")])
    assert code == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["run_count"] == 12
    assert payload["total_distance_km"] > 0


def test_cli_load_and_race(capsys):
    assert main(["load-recovery", "--input", str(SAMPLE / "load_recovery.json")]) == 0
    load = json.loads(capsys.readouterr().out)
    assert load["recommendation"] in {"rest", "easy", "normal", "quality"}

    assert main(["race-readiness", "--input", str(SAMPLE / "race_readiness.json"), "--target", "half"]) == 0
    race = json.loads(capsys.readouterr().out)
    assert race["target"] == "half"
    assert 0 <= race["score"] <= 100
