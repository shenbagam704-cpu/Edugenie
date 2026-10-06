import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    gemini_api_key: str | None = os.getenv("GEMINI_API_KEY")
    gemini_model: str = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")
    local_explanation_enabled: bool = os.getenv(
        "LOCAL_EXPLANATION_ENABLED", "false"
    ).lower() == "true"
    local_explanation_model: str = os.getenv(
        "LOCAL_EXPLANATION_MODEL", "MBZUAI/LaMini-Flan-T5-783M"
    )
    max_input_chars: int = int(os.getenv("MAX_INPUT_CHARS", "20000"))


settings = Settings()
