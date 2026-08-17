"""Motor de política y enrutamiento.

Este módulo es la **única** implementación de la semántica de política del
proyecto. El servidor MCP autocontenido que se distribuye dentro de cada
paquete (`plugins/<id>/runtime/mcp_server.py`) no reimplementa estas reglas:
`render.py` copia literalmente el código fuente de `_matches` y de
`classify_action` al generar ese archivo, de modo que la CLI y el paquete
distribuido no pueden responder cosas distintas a la misma pregunta.

Si cambias una de estas dos funciones, `agentic-plugins sync` regenera los seis
servidores y CI falla mientras no lo hagas.
"""

from __future__ import annotations


def _matches(text: str, item: str) -> bool:
    normalized_text = text.casefold().replace("_", "-")
    variants = {item.casefold(), item.casefold().replace("-", " ")}
    return any(variant in normalized_text for variant in variants)


def classify_action(plugin: dict, action: str) -> dict:
    denied = next((item for item in plugin["policy"]["denied"] if _matches(action, item)), None)
    approval = next((item for item in plugin["policy"]["approval_required"] if _matches(action, item)), None)
    decision = "denied" if denied else "approval-required" if approval else "allowed"
    return {"action": action, "decision": decision, "matched": denied or approval}


def route_request(plugin: dict, text: str) -> dict:
    """Decide si el plugin debe activarse y si la solicitud toca un gate humano.

    Una palabra negativa solo desactiva cuando no hay ninguna señal positiva ni
    ninguna acción sujeta a aprobación: preguntar por el clima no activa nada,
    pero «publica el release aunque haga mal clima» sigue siendo una publicación
    y debe detenerse en su gate.
    """
    positives = [word for word in plugin["activation"]["keywords"] if _matches(text, word)]
    negatives = [word for word in plugin["activation"]["negative_keywords"] if _matches(text, word)]
    approvals = [word for word in plugin["policy"]["approval_required"] if _matches(text, word)]
    activate = bool(positives or approvals) and not (negatives and not positives and not approvals)
    return {
        "activate": activate,
        "approval": bool(approvals),
        "positive_matches": positives,
        "negative_matches": negatives,
        "approval_matches": approvals,
    }
