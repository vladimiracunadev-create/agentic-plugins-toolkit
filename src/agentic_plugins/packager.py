from __future__ import annotations

import hashlib
import json
import zipfile
from pathlib import Path

SKIP = {"__pycache__", ".DS_Store"}


def package_plugin(root: Path, plugin: dict, output: Path) -> tuple[Path, str]:
    source = root / "plugins" / plugin["id"]
    output.mkdir(parents=True, exist_ok=True)
    destination = output / f"{plugin['id']}-{plugin['version']}.zip"
    with zipfile.ZipFile(
        destination, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9
    ) as archive:
        for path in sorted(source.rglob("*")):
            if not path.is_file() or any(part in SKIP for part in path.parts):
                continue
            relative = Path(plugin["id"]) / path.relative_to(source)
            info = zipfile.ZipInfo(
                str(relative).replace("\\", "/"), date_time=(1980, 1, 1, 0, 0, 0)
            )
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            archive.writestr(info, path.read_bytes())
    digest = hashlib.sha256(destination.read_bytes()).hexdigest()
    return destination, digest


def write_checksums(output: Path, values: list[tuple[Path, str]]) -> Path:
    path = output / "checksums.json"
    path.write_text(
        json.dumps({item.name: digest for item, digest in values}, indent=2) + "\n",
        encoding="utf-8",
    )
    return path
