from __future__ import annotations

import json
from pathlib import Path

from .policy import route_request


def evaluate_plugin(root: Path, plugin: dict) -> list[dict]:
    path = root / "plugins" / plugin["id"] / "evals" / "cases.jsonl"
    results = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        case = json.loads(line)
        actual = route_request(plugin, case["input"])
        expected = case["expected"]
        passed = (
            actual["activate"] == expected["activate"]
            and actual["approval"] == expected["approval"]
        )
        results.append(
            {
                "id": case["id"],
                "line": line_number,
                "passed": passed,
                "expected": expected,
                "actual": actual,
            }
        )
    return results
