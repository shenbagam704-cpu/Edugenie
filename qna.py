from ai_client import generate_text

SYSTEM_STYLE = """
You are EduGenie, a student-friendly educational assistant.
Answer the user's academic question accurately and concisely.
Use simple language, short sections, and examples when useful.
Do not pretend to know facts you are uncertain about.
"""


async def answer_question(question: str) -> str:
    prompt = f"""
{SYSTEM_STYLE}

Student question:
{question}

Give a direct answer first, followed by a short explanation if helpful.
"""
    return await generate_text(prompt)
