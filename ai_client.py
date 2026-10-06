from functools import lru_cache

from config import settings


class GeminiServiceError(RuntimeError):
    pass


@lru_cache(maxsize=1)
def get_client():
    try:
        from google import genai
    except ImportError as exc:
        raise GeminiServiceError(
            "The Google GenAI SDK is not installed. Run: pip install -r requirements.txt"
        ) from exc

    if not settings.gemini_api_key:
        raise GeminiServiceError(
            "GEMINI_API_KEY is not configured. Copy .env.example to .env and add your key."
        )

    return genai.Client(api_key=settings.gemini_api_key)


def _validate_input(text: str) -> str:
    value = text.strip()
    if not value:
        raise ValueError("Input cannot be empty.")
    if len(value) > settings.max_input_chars:
        raise ValueError(
            f"Input is too long. Maximum supported length is {settings.max_input_chars} characters."
        )
    return value


async def generate_text(prompt: str) -> str:
    prompt = _validate_input(prompt)

    try:
        from google.genai import types
        response = get_client().models.generate_content(
            model=settings.gemini_model,
            contents=prompt,
            config=types.GenerateContentConfig(temperature=0.3),
        )
        text = (response.text or "").strip()
        if not text:
            raise GeminiServiceError("Gemini returned an empty response.")
        return text
    except GeminiServiceError:
        raise
    except Exception as exc:
        raise GeminiServiceError(f"Gemini request failed: {exc}") from exc


async def generate_structured(prompt: str, response_schema) -> str:
    prompt = _validate_input(prompt)

    try:
        from google.genai import types
        response = get_client().models.generate_content(
            model=settings.gemini_model,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.2,
                response_mime_type="application/json",
                response_schema=response_schema,
            ),
        )
        text = (response.text or "").strip()
        if not text:
            raise GeminiServiceError("Gemini returned an empty structured response.")
        return text
    except GeminiServiceError:
        raise
    except Exception as exc:
        raise GeminiServiceError(f"Gemini structured request failed: {exc}") from exc
