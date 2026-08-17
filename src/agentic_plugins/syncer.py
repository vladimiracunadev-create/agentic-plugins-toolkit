from __future__ import annotations

from pathlib import Path

from .render import expected_views


def sync(root: Path, check: bool = False) -> list[str]:
    drift = []
    for path, expected in expected_views(root).items():
        try:
            current = path.read_text(encoding="utf-8")
        except OSError:
            current = None
        if current != expected:
            drift.append(str(path.relative_to(root)))
            if not check:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(expected, encoding="utf-8", newline="\n")
    return drift


def check_sync(root: Path) -> list[str]:
    return sync(root, check=True)
