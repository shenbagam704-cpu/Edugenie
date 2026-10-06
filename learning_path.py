import json

from ai_client import generate_structured
from schemas import LearningPathResponse


async def get_learning_recommendations(topic: str) -> LearningPathResponse:
    prompt = f"""
Create a personalized learning path for the topic "{topic}".

Requirements:
- Start at beginner level and progress toward advanced level.
- Provide 4 to 6 ordered learning steps.
- For each step include topics, estimated study time, learning goals,
  and 2 or 3 useful resources.
- Resource URLs may be official documentation, reputable educational sites,
  or well-known books. If you are not confident in an exact URL, leave url empty.
- Keep the plan practical and suitable for a self-learner.
- Return ONLY JSON matching the requested schema.
"""
    raw = await generate_structured(prompt, LearningPathResponse)
    try:
        return LearningPathResponse.model_validate(json.loads(raw))
    except Exception as exc:
        raise ValueError(f"Invalid learning-path JSON returned by Gemini: {exc}") from exc
