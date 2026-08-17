"""Panel local de inspección del catálogo.

Sirve `site/` como archivos estáticos y expone `/api/plugins` y `/healthz`.

El panel **no implementa autenticación**. Por eso solo enlaza a loopback y salir
de ahí exige declarar `AGENTIC_PLUGINS_ALLOW_REMOTE_BIND=1` de forma explícita:
que el binario acepte `--host 0.0.0.0` sin fricción convierte una herramienta de
inspección local en un servicio expuesto sin que nadie lo haya decidido.
"""

from __future__ import annotations

import ipaddress
import json
import os
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from .catalog import load_catalog

ALLOW_REMOTE_ENV = "AGENTIC_PLUGINS_ALLOW_REMOTE_BIND"


def is_loopback(host: str) -> bool:
    if host in {"localhost", ""}:
        return True
    try:
        return ipaddress.ip_address(host).is_loopback
    except ValueError:
        return False


def ensure_bind_is_allowed(host: str) -> None:
    if is_loopback(host):
        return
    if os.environ.get(ALLOW_REMOTE_ENV) == "1":
        return
    raise ValueError(
        f"El panel no tiene autenticación: use loopback o declare {ALLOW_REMOTE_ENV}=1 "
        f"si de verdad quiere exponer {host}."
    )


def serve(root: Path, host: str, port: int) -> None:
    ensure_bind_is_allowed(host)
    catalog = load_catalog(root)
    site = root / "site"
    payload = json.dumps(catalog, ensure_ascii=False).encode("utf-8")

    class Handler(SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=str(site), **kwargs)

        def _send(self, body: bytes, content_type: str) -> None:
            self.send_response(200)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(body)))
            self.send_header("X-Content-Type-Options", "nosniff")
            self.end_headers()
            self.wfile.write(body)

        def do_GET(self):
            if self.path.split("?")[0] == "/api/plugins":
                self._send(payload, "application/json; charset=utf-8")
                return
            if self.path.split("?")[0] == "/healthz":
                self._send(b'{"status":"ok"}', "application/json; charset=utf-8")
                return
            super().do_GET()

        # La firma la fija BaseHTTPRequestHandler; silenciar el log es intencional.
        def log_message(self, fmt, *args):
            pass

    print(f"Control center: http://{host}:{port}")
    ThreadingHTTPServer((host, port), Handler).serve_forever()
