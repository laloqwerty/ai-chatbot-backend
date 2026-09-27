# Chatbot Backend

FastAPI backend for a chatbot using LangChain and Ollama.

## Requirements

- uv
- Ollama installed locally
- Git

On Windows, install uv with either:

```powershell
winget install --id=astral-sh.uv -e
```

or:

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

## 1) Clone the repository

```bash
git clone <repo-url>
cd chatbot-backend
```

## 2) Create the environment

```bash
uv sync
```

## 3) Configure environment variables

Copy the example file:

```bash
copy .env.example .env
```

Then edit `.env` if needed:

```env
OLLAMA_MODEL=gemma4:e4b
OLLAMA_BASE_URL=http://localhost:11434
```

## 4) Pull the required Ollama model

```bash
ollama pull gemma4:e4b
```

## 5) Run the app

```bash
uv run uvicorn app.main:app --reload
```

The API will be available at:

- http://localhost:8000

## API endpoint

```http
POST /chat
```

Example body:

```json
{
  "message": "Hello!",
  "session_id": "user-123"
}
```

## Notes

- Keep your real `.env` file local and do not commit it.
- The repository includes `.env.example` as a safe template.
- The app uses the Ollama model configured in `.env` or falls back to `gemma4:e4b`.
