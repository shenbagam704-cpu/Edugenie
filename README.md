# EduGenie — Google Gemini Powered Learning Assistant

EduGenie is a lightweight FastAPI web application based on the supplied project document. It provides:

- Question answering
- Beginner-friendly concept explanation
- 3-question MCQ generation with 4 options each
- Passage summarization
- Beginner-to-advanced learning recommendations

The original specification names Gemini 1.5 Pro and LaMini-Flan-T5-783M. The implementation keeps the same architecture and module responsibilities, but uses Google's current `google-genai` SDK and makes the Gemini model configurable through `.env`.

## Project structure

```text
EduGenie/
├── main.py
├── config.py
├── ai_client.py
├── schemas.py
├── qna.py
├── explanation_module.py
├── quiz_module.py
├── summary_module.py
├── learning_path.py
├── requirements.txt
├── requirements-local.txt
├── .env.example
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── README.md
├── templates/
│   └── index.html
├── static/
│   ├── app.js
│   └── style.css
└── tests/
    └── test_app.py
```

## 1. Prerequisites

- Python 3.10+
- VS Code
- A Gemini API key
- Internet access for Gemini API calls

## 2. Create a virtual environment

### Windows PowerShell

```powershell
py -3.12 -m venv .venv
.venv\Scripts\Activate.ps1
```

### macOS/Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 4. Configure Gemini

Copy `.env.example` to `.env`:

### Windows PowerShell

```powershell
Copy-Item .env.example .env
```

### macOS/Linux

```bash
cp .env.example .env
```

Open `.env` and set:

```env
GEMINI_API_KEY=your_key_here
GEMINI_MODEL=gemini-3.8-flash
```

Do not commit `.env` to Git.

## 5. Run the application

```bash
uvicorn main:app --reload
```

Open:

```text
http://127.0.0.1:8000
```

FastAPI's interactive API documentation is also available at:

```text
http://127.0.0.1:8000/docs
```

## 6. Test

Run automated tests:

```bash
pytest -q
```

The tests verify the home page, health endpoint, and request validation without making a Gemini API call; the Google SDK is imported lazily so these basic tests can run before cloud dependencies are installed.

For an end-to-end manual test, use the browser UI and try:

- Q&A: `Which is the largest ocean?`
- Explain: `Pythagoras theorem`
- Quiz: paste a short textbook paragraph
- Summarize: paste a long educational paragraph
- Learning path: `SQL`

## 7. Optional LaMini local explanation model

The original document specifies `LaMini-Flan-T5-783M` for concept explanation. To enable that optional local path:

```bash
pip install -r requirements-local.txt
```

Then edit `.env`:

```env
LOCAL_EXPLANATION_ENABLED=true
LOCAL_EXPLANATION_MODEL=MBZUAI/LaMini-Flan-T5-783M
```

The model is downloaded by Hugging Face the first time it is used, so the first explanation request may take longer and require substantial disk/RAM. If the local model cannot load, EduGenie automatically falls back to Gemini.

## 8. API examples

### Q&A

```bash
curl -X POST http://127.0.0.1:8000/qa \
  -H "Content-Type: application/json" \
  -d "{\"text\":\"What is photosynthesis?\"}"
```

### Explain

```bash
curl -X POST http://127.0.0.1:8000/explain \
  -H "Content-Type: application/json" \
  -d "{\"text\":\"Explain the Pythagoras theorem.\"}"
```

### Quiz

```bash
curl -X POST http://127.0.0.1:8000/quiz \
  -H "Content-Type: application/json" \
  -d "{\"text\":\"Water boils at 100 degrees Celsius at standard atmospheric pressure.\"}"
```

### Summary

```bash
curl -X POST http://127.0.0.1:8000/summarize \
  -H "Content-Type: application/json" \
  -d "{\"text\":\"Paste your educational passage here.\"}"
```

### Learning path

```bash
curl -X POST http://127.0.0.1:8000/learn/recommendations \
  -H "Content-Type: application/json" \
  -d "{\"text\":\"SQL\"}"
```

## 9. Docker

Create `.env` first, then:

```bash
docker compose up --build
```

Open:

```text
http://127.0.0.1:8000
```

## Notes

The application intentionally keeps the Gemini model name in configuration because model availability changes over time. The API layer also validates quiz output before returning it to the browser, so malformed structured responses become clear server errors instead of silently breaking the UI.
