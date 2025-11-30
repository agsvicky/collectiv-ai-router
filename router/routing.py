from typing import Final

from .models import ChatRequest

# Alle unterstützten Provider (inkl. "auto" für Auto-Routing)
SUPPORTED_PROVIDERS: Final[set[str]] = {
    "auto",
    "openai",
    "gemini",
    "mistral",
    "meta",
    "deepseek",
    "custom",
}


def choose_provider(request: ChatRequest) -> str:
    """Small but explicit routing logic for the CollectiVAI Router.

    - If the client sends provider != "auto", we respect that (after validation).
    - If provider == "auto", we choose based on mode + topic.
    """

    # Normalisieren / absichern
    provider = (request.provider or "").strip().lower()
    mode = (request.mode or "").strip().lower()
    topic = (request.topic or "").strip().lower()

    if provider not in SUPPORTED_PROVIDERS:
        raise ValueError(f"Unsupported provider: {provider!r}")

    # 1) Explizite Provider-Wahl des Clients
    if provider != "auto":
        return provider

    # 2) Auto-Routing – bewusst simpel, aber gut erweiterbar
    #    -> Hier kannst du später Costs, Scores, Policies etc. einbauen.

    if mode == "technical":
        # Bevorzugt für Code / Security / Tools
        return "mistral"

    if topic in {"democracy", "economy"}:
        return "openai"

    if topic in {"climate", "research"}:
        return "gemini"

    # 3) Fallback – robustes Default
    return "openai"
