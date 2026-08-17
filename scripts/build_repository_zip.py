from __future__ import annotations

import argparse
import hashlib
import zipfile
from pathlib import Path

SKIP_PARTS = {".git", ".venv", "__pycache__", "build", "dist", ".ruff_cache", ".pytest_cache"}


def should_skip(path: Path) -> bool:
    return any(
        part in SKIP_PARTS or part.endswith(".egg-info") for part in path.parts
    )


def build(root: Path, output: Path) -> tuple[int, str]:
    files = [
        path
        for path in sorted(root.rglob("*"))
        if path.is_file() and not should_skip(path.relative_to(root))
    ]
    with zipfile.ZipFile(
        output, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9
    ) as archive:
        for path in files:
            relative = Path(root.name) / path.relative_to(root)
            info = zipfile.ZipInfo(
                str(relative).replace("\\", "/"),
                date_time=(1980, 1, 1, 0, 0, 0),
            )
            info.compress_type = zipfile.ZIP_DEFLATED
            mode = 0o755 if path.suffix == ".sh" else 0o644
            info.external_attr = mode << 16
            archive.writestr(info, path.read_bytes())
    return len(files), hashlib.sha256(output.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        type=Path,
        help="Ruta del ZIP; por defecto se crea junto al repositorio.",
    )
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    output = (
        args.output.expanduser().resolve()
        if args.output
        else root.parent / f"{root.name}.zip"
    )
    count, digest = build(root, output)
    print(f"{output}")
    print(f"files={count}")
    print(f"sha256={digest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
