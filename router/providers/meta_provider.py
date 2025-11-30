import asyncio
from typing import Optional


async def complete(prompt: str, model_id: Optional[str]) -> tuple[str, str]:
    await asyncio.sleep(0.05)
    model = model_id or "llama-3.1-8b"
    return f"[Meta / {model}] Demo reply for: {prompt[:80]}...", model
