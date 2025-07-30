import json
import asyncio
from groq import AsyncGroq
from app.core.config import get_settings

settings = get_settings()
client = AsyncGroq(api_key=settings.groq_api_key)

SYSTEM_PROMPT = (
    "You are a cyber-threat analyst assistant. "
    "You will be given up-to-date ransomware intelligence. "
    "Answer concisely and add actionable insights."
)

def _trim_context(data, max_chars: int = 4_000) -> str:
    """Compact JSON + hard length limit."""
    text = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    return text[:max_chars] + ("…" if len(text) > max_chars else "")

async def ask_llm(data, question: str) -> str:
    context = _trim_context(data)
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"Context:\n{context}\n\nQuestion:\n{question}"},
    ]
    resp = await client.chat.completions.create(
        model=settings.model_id,
        messages=messages,
        max_tokens=settings.max_tokens,
        temperature=settings.temperature,
    )
    return resp.choices[0].message.content

async def ask_llm_stream(context: str, question: str):
    """Yield complete sentences instead of raw tokens."""
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"Context:\n{context}\n\nQuestion:\n{question}"},
    ]
    stream = await client.chat.completions.create(
        model=settings.model_id,
        messages=messages,
        max_tokens=settings.max_tokens,
        temperature=settings.temperature,
        stream=True,
    )

    buffer = ""
    async for chunk in stream:
        text = chunk.choices[0].delta.content or ""
        buffer += text

        if buffer.endswith((".", "!", "?", "\n")):
            yield f"data: {buffer.strip()}\n\n"
            buffer = ""

    if buffer.strip():
        yield f"data: {buffer.strip()}\n\n"
    yield "data: [DONE]\n\n"