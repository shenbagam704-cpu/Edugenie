from ai_client import generate_text


async def summarize_text(text: str) -> str:
    prompt = f"""
You are EduGenie, an educational summarizer.

Summarize the following passage for a student revising for an exam.
Preserve the important facts, definitions, relationships, and conclusions.
Remove repetition and unnecessary wording.
Use a short heading and bullet points when that improves readability.
Do not add facts that are not supported by the passage.

PASSAGE:
{text}
"""
    return await generate_text(prompt)
