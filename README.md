# circus_portfolio_backend

FastAPI backend for collecting and retrieving portfolio reviews, with HuggingFace sentiment analysis.

## Setup

**1. Create and activate a virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Configure environment variables**

Copy `.env` and set your HuggingFace API token:
```bash
echo "HF_TOKEN=your_token_here" > .env
```

## Running the server

```bash
uvicorn main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

## API

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/reviews` | Submit a review |
| `GET` | `/reviews` | Retrieve all reviews |

**POST `/reviews` request body:**
```json
{
  "message": "Great work!",
  "name": "Jane Doe",
  "organisation": "Acme Corp",
  "project_id": 1
}
```
`name`, `organisation`, and `project_id` are optional.