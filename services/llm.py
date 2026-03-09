import logging
import os
import httpx
from typing import TypedDict

logger = logging.getLogger(__name__)


class SentimentLabel(TypedDict):
    label: str
    score: float


SentimentResult = list[list[SentimentLabel]]

HF_TOKEN = os.getenv("HF_TOKEN")
HF_BASE_URL = "https://router.huggingface.co/hf-inference/models"


async def get_sentiment(message: str) -> SentimentResult:
    model = "finiteautomata/bertweet-base-sentiment-analysis"
    logger.info("Requesting sentiment analysis")
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{HF_BASE_URL}/{model}",
            headers={
                "Authorization": f"Bearer {HF_TOKEN}",
                "Content-Type": "application/json",
            },
            json={"inputs": message},
        )
        response.raise_for_status()
        data: SentimentResult = response.json()
        positive_analysis = next(analysis for analysis in data[0] if analysis["label"] == "POS")

        logger.debug("Sentiment result: %s", data)

        return positive_analysis["score"]


async def detect_language(text: str) -> str:
    model = "xlm-roberta-base"

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{HF_BASE_URL}/{model}",
            headers={
                "Authorization": f"Bearer {HF_TOKEN}",
                "Content-Type": "application/json",
            },
            json={"inputs": text},
        )

        result = response.json()
        logger.debug("Detected language response: ", result)
        return result
    # return result[0][0]["label"]


async def translate_message(message: str) -> dict:
    """Translate message to EN, FR, DE"""

    source_lang = await detect_language(message)

    translations = {
        "original": message,
        "source_lang": source_lang,
        "en": message if source_lang == "en" else await translate(message, source_lang, "en"),
        "fr": message if source_lang == "fr" else await translate(message, source_lang, "fr"),
        "de": message if source_lang == "de" else await translate(message, source_lang, "de"),
    }
    return translations


async def translate(text: str, source_lang: str, target_lang: str) -> str:
    """Translate from source to target language"""

    model = f"Helsinki-NLP/opus-mt-{source_lang}-{target_lang}"

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{HF_BASE_URL}/{model}",
            headers={
                "Authorization": f"Bearer {HF_TOKEN}",
                "Content-Type": "application/json",
            },
            json={"inputs": text},
        )

        result = response.json()
        logger.debug(f"Translation result: {result}")
        return result
    return result[0][0]["translation_text"]
