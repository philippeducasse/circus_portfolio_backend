import os
import httpx
from dotenv import load_dotenv

load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")
HF_MODEL_URL = "https://router.huggingface.co/hf-inference/models/finiteautomata/bertweet-base-sentiment-analysis"


async def get_sentiment(message: str):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            HF_MODEL_URL,
            headers={
                "Authorization": f"Bearer {HF_TOKEN}",
                "Content-Type": "application/json",
            },
            json={"inputs": message},
        )
        response.raise_for_status()
        return response.json()