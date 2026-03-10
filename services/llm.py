import logging
import os
from typing import TypedDict

from huggingface_hub import InferenceClient

logger = logging.getLogger(__name__)


class SentimentLabel(TypedDict):
    label: str
    score: float


SentimentResult = list[list[SentimentLabel]]

HF_BASE_URL = "https://router.huggingface.co/hf-inference/models"

client = InferenceClient(
    provider="hf-inference",
    api_key=os.environ["HF_TOKEN"],
)


async def get_sentiment(message: str) -> float:
    try:
        sentiment = client.text_classification(
            message, model="finiteautomata/bertweet-base-sentiment-analysis"
        )
        positive_message_probability = next(s for s in sentiment if s.label == "POS")
        return positive_message_probability.score
    except Exception as e:
        logger.error(f"Sentiment analysis failed for message '{message}': {e}")
        return 0.0


async def detect_language(text: str) -> str:
    detected_language = client.text_classification(
        text, model="papluca/xlm-roberta-base-language-detection"
    )

    return detected_language[0]["label"]


async def translate_message(message: str) -> dict:
    """Translate message to EN, FR, DE"""

    source_lang = await detect_language(message)

    if source_lang != "en":
        english_translation = await translate(message, source_lang, "en")
    else:
        english_translation = message

    translations = {
        "original": message,
        "source_lang": source_lang,
        "en": english_translation,
        "fr": message if source_lang == "fr" else await translate(english_translation, "en", "fr"),
        "de": message if source_lang == "de" else await translate(english_translation, "en", "de"),
    }

    return translations


async def translate(text: str, source_lang: str, target_lang: str) -> str:
    """Translate from source to target language"""

    model = f"Helsinki-NLP/opus-mt-{source_lang}-{target_lang}"

    translation = client.translation(text, model=model)

    return translation.translation_text
