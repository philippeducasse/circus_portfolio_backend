# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run dev server
uvicorn main:app --reload

# Run with custom port
uvicorn main:app --reload --port 8000
```

## Architecture

FastAPI backend for a portfolio review/feedback system. Single-purpose: collect and retrieve text reviews with HuggingFace sentiment analysis.

- **`main.py`** — app entrypoint, CORS config, route definitions (`POST /reviews`, `GET /reviews`)
- **`database.py`** — SQLAlchemy engine + `get_db` dependency (SQLite `portfolio.db`)
- **`models.py`** — `Review` ORM model (maps to existing `reviews` table)
- **`schemas.py`** — `ReviewCreate` (input) and `ReviewOut` (output) Pydantic models
- **`services/llm.py`** — async HuggingFace API call for sentiment analysis; failure is non-blocking (review is always saved)

## Key Details

- SQLite database `portfolio.db` is in the project root; schema is created on startup via `Base.metadata.create_all`
- HuggingFace token is loaded from `.env` (`HF_TOKEN`); model: `finiteautomata/bertweet-base-sentiment-analysis`
- CORS allows: `http://localhost:3000`, `http://127.0.0.1:3000`, `https://philippeducasse.com`
- Date stored as TEXT in format `dd-mm-yy HH:MM:SS` to match legacy PHP data in the DB