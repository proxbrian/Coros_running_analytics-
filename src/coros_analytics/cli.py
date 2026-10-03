from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from coros_analytics.fit_summary import summarize_fit
from coros_analytics.load_recovery import assess_load_recovery
from coros_analytics.race_readiness import assess_race_readiness
from coros_analytics.weekly_review import build_weekly_review


def _load_json(path: str) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _print(data: dict[str, Any]) -> None:
    json.dump(data, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="coros-analytics",
        description="Local running analytics for agents backed by official COROS MCP.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    weekly = sub.add_parser("weekly-review", help="Aggregate run volume and pace by week")
    weekly.add_argument("--input", required=True, help="JSON file with activities[]")

    load = sub.add_parser("load-recovery", help="Recommend today intensity from load/recovery")
    load.add_argument("--input", required=True, help="JSON file with load/recovery fields")

    race = sub.add_parser("race-readiness", help="Score readiness for a race distance")
    race.add_argument("--input", required=True, help="JSON file with readiness fields")
    race.add_argument(
        "--target",
        choices=("5k", "10k", "half", "marathon"),
        help="Override target distance in the JSON payload",
    )

    fit = sub.add_parser("fit-summary", help="Summarize a FIT activity file")
    fit.add_argument("--fit", required=True, help="Path to .fit file")

    args = parser.parse_args(argv)

    if args.command == "weekly-review":
        _print(build_weekly_review(_load_json(args.input)).to_dict())
        return 0
    if args.command == "load-recovery":
        _print(assess_load_recovery(_load_json(args.input)).to_dict())
        return 0
    if args.command == "race-readiness":
        payload = _load_json(args.input)
        if args.target:
            payload["target"] = args.target
        _print(assess_race_readiness(payload).to_dict())
        return 0
    if args.command == "fit-summary":
        _print(summarize_fit(args.fit))
        return 0

    parser.error(f"Unknown command: {args.command}")
    return 2


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
