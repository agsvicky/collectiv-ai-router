import os
from functools import lru_cache
from typing import List


class Settings:
    """Central configuration for the CollectiVAI Router.

    Values are loaded from environment variables. In production, configure these
    via your hosting platform (Cloudflare, Docker, etc.).
    """

    # CORS
    allowed_origins: List[str]

    # Provider API keys
    openai_api_key: str | None
    gemini_api_key: str | None
    mistral_api_key: str | None
    meta_api_key: str | None
    deepseek_api_key: str | None

    # Optional custom backend
    custom_backend_url: str | None
    custom_backend_token: str | None

    def __init__(self) -> None:
        origins = os.getenv("ROUTER_ALLOWED_ORIGINS", "")
        self.allowed_origins = [o.strip() for o in origins.split(",") if o.strip()]

        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")
        self.mistral_api_key = os.getenv("MISTRAL_API_KEY")
        self.meta_api_key = os.getenv("META_API_KEY")
        self.deepseek_api_key = os.getenv("DEEPSEEK_API_KEY")

        self.custom_backend_url = os.getenv("CUSTOM_BACKEND_URL")
        self.custom_backend_token = os.getenv("CUSTOM_BACKEND_TOKEN")


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
