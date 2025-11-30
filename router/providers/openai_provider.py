import asyncio
from typing import Optional

# In a real implementation you would import the OpenAI client and use the
# OPENAI_API_KEY from the environment. Here we keep it as a placeholder to
# avoid accidental misuse in public repos.

async def complete(prompt: str, model_id: Optional[str]) -> tuple[str, str]:
    """Placeholder OpenAI provider.

    Replace this with a real OpenAI API call in your private deployment.
    """
    await asyncio.sleep(0.05)
    model = model_id or "gpt-4.1"
    return f"[OpenAI / {model}] Demo reply for: {prompt[:80]}...", model
