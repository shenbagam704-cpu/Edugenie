from ai_client import generate_text
from config import settings


def _local_explain(topic: str) -> str:
    # Optional dependency path. Imports are intentionally lazy so the normal
    # Gemini-only installation stays lightweight.
    from transformers import pipeline

    generator = pipeline(
        "text2text-generation",
        model=settings.local_explanation_model,
        max_new_tokens=180,
    )
    prompt = (
        "Explain this educational topic in simple language for a beginner: "
        f"{topic}"
    )
    result = generator(prompt)[0]["generated_text"]
    return result.strip()


async def explain_concept(topic: str) -> str:
    if settings.local_explanation_enabled:
        try:
            return _local_explain(topic)
        except Exception:
            # Fall back to Gemini if the optional local model is unavailable.
            pass

    prompt = f"""
Explain the following concept to a beginner.

Topic:
{topic}

Use this structure:
1. Simple definition
2. How it works
3. Easy example
4. One key point to remember

Avoid unnecessary jargon and keep the explanation concise.
"""
    return await generate_text(prompt)
