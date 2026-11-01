FROM python:3.15-slim

WORKDIR /app
COPY . .
RUN python -m pip install --no-cache-dir .

# El panel no tiene autenticación y por eso `serve` se niega a enlazar fuera de
# loopback salvo declaración explícita. Dentro del contenedor 0.0.0.0 es la única
# dirección alcanzable desde el host, así que el opt-in se declara aquí — y
# compose.yaml publica el puerto **solo** en el loopback del host.
ENV AGENTIC_PLUGINS_ALLOW_REMOTE_BIND=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONUTF8=1

USER 65532:65532
EXPOSE 8787

HEALTHCHECK --interval=10s --timeout=3s --start-period=5s --retries=5 \
  CMD python -c "import urllib.request,sys; sys.exit(0 if urllib.request.urlopen('http://127.0.0.1:8787/healthz', timeout=2).status == 200 else 1)"

CMD ["agentic-plugins", "serve", "--host", "0.0.0.0", "--port", "8787"]
