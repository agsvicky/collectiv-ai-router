from typing import List, Optional, Literal
from pydantic import BaseModel, Field, field_validator


# --- Type Aliases für klarere Doku & Validierung ---

Mode = Literal["ethical", "research", "technical"]
Provider = Literal["auto", "openai", "gemini", "mistral", "meta", "deepseek", "custom"]
Topic = Literal["democracy", "climate", "economy", "security", "research", "health"]


class ChatRequest(BaseModel):
    """Incoming chat request from the CollectiVAI app."""

    prompt: str = Field(..., min_length=1, description="User prompt text")
    mode: Mode = Field(..., description="Routing mode (ethical, research, technical)")
    provider: Provider = Field(
        ...,
        description=(
            "Requested provider "
            "(auto, openai, gemini, mistral, meta, deepseek, custom)"
        ),
    )
    topic: Topic = Field(
        ...,
        description=(
            "High-level topic "
            "(democracy, climate, economy, security, research, health)"
        ),
    )
    modelId: Optional[str] = Field(
        None,
        description="Optional explicit model ID (e.g. gpt-4.1, gemini-1.5-pro, mistral-large).",
    )
    serviceProfile: Optional[str] = Field(
        None,
        description="Civic service profile (city_service, ngo_lab, research_unit, etc.)",
    )

    # --- Validators / Normalisierung ---

    @field_validator("prompt")
    @classmethod
    def strip_prompt(cls, v: str) -> str:
        """Trim whitespace from the prompt."""
        v = v.strip()
        if not v:
            raise ValueError("Prompt must not be empty")
        return v

    @field_validator("mode", "provider", "topic", mode="before")
    @classmethod
    def normalize_lower(cls, v: str) -> str:
        """Normalize routing fields: strip + lowercase."""
        if v is None:
            return v
        return v.strip().lower()

    model_config = {
        "extra": "forbid",  # Unbekannte Felder im Request werden abgelehnt
    }


class RoutingInfo(BaseModel):
    """Metadata about the routing decision for this request."""

    reason: Optional[str] = None
    filters: Optional[List[str]] = None
    latencyMs: Optional[int] = Field(
        None,
        description="Measured end-to-end latency for the provider call in milliseconds.",
    )


class ChatResponse(BaseModel):
    """Response returned to the CollectiVAI app."""

    reply: str = Field(..., description="Final assistant message returned to the user.")
    providerUsed: str = Field(
        ...,
        description="The provider that was actually used for this request.",
    )
    model: str = Field(
        ...,
        description="The concrete model name / ID used by the provider.",
    )
    routingInfo: Optional[RoutingInfo] = Field(
        None,
        description="Optional metadata describing how and why this request was routed.",
    )

    model_config = {
        "extra": "ignore",  # Falls du später serverseitig Felder hinzufügst, wird der Client nicht kaputt
    }
