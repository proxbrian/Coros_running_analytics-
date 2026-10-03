from types import SimpleNamespace

import fitparse

from coros_analytics import fit_summary


class _FakeMessage:
    def __init__(self, name: str, fields: dict):
        self.name = name
        self._fields = fields

    def __iter__(self):
        for key, value in self._fields.items():
            yield SimpleNamespace(name=key, value=value)


class _FakeFitFile:
    def __init__(self, _path: str):
        self._messages = [
            _FakeMessage(
                "session",
                {
                    "total_distance": 5000.0,
                    "total_elapsed_time": 1500.0,
                    "avg_speed": 3.333,
                    "avg_heart_rate": 150,
                    "max_heart_rate": 175,
                    "total_ascent": 40,
                },
            ),
            _FakeMessage("record", {"speed": 3.2, "heart_rate": 145, "altitude": 10, "cadence": 85}),
            _FakeMessage("record", {"speed": 3.4, "heart_rate": 155, "altitude": 12, "cadence": 88}),
        ]

    def get_messages(self):
        return self._messages


def test_summarize_fit(monkeypatch, tmp_path):
    fit_path = tmp_path / "sample.fit"
    fit_path.write_bytes(b"fit-placeholder")
    monkeypatch.setattr(fitparse, "FitFile", _FakeFitFile)

    summary = fit_summary.summarize_fit(fit_path)
    assert summary["distance_km"] == 5.0
    assert summary["avg_hr"] == 150
    assert summary["record_count"] == 2
    assert summary["avg_pace_s_per_km"] is not None
