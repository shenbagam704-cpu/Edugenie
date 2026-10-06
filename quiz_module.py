import json

from ai_client import generate_structured
from schemas import QuizResponse


async def generate_quiz(passage: str) -> QuizResponse:
    prompt = f"""
Generate exactly 3 multiple-choice questions from the passage below.

Rules:
- Each question must have exactly 4 options.
- Exactly one option must be the correct answer.
- The correct_answer value must exactly match one option.
- Include a short explanation for the correct answer.
- Questions must test the passage rather than unrelated background knowledge.
- Make distractors plausible but clearly incorrect based on the passage.
- Return ONLY JSON matching the requested schema.

PASSAGE:
{passage}
"""
    raw = await generate_structured(prompt, QuizResponse)
    try:
        result = QuizResponse.model_validate(json.loads(raw))
    except Exception as exc:
        raise ValueError(f"Invalid quiz JSON returned by Gemini: {exc}") from exc

    for item in result.questions:
        if item.correct_answer not in item.options:
            raise ValueError("Gemini returned a correct answer not present in the options.")
    return result
