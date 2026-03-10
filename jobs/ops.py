import asyncio
import logging
from datetime import datetime
from typing import Optional

from dagster import op

from db.models import Review
from services.llm import get_sentiment, translate_message

logger = logging.getLogger(__name__)


@op
def translate_op(message: str) -> dict:
    """Translate message to EN, FR, DE"""
    return asyncio.run(translate_message(message))


@op
def sentiment_op(translations: dict) -> float:
    """Get sentiment of English translation"""
    return asyncio.run(get_sentiment(translations["en"]))


@op
def save_review_op(
    translations: dict,
    sentiment_score: float,
    db_session,
    name: Optional[str],
    organisation: Optional[str],
    project_id: Optional[int],
) -> int:
    """Save review to database"""
    positive_message = sentiment_score > 0.9
    logger.info(
        f"Sentiment score: {sentiment_score:.3f}, positive_message: {positive_message}, message: {translations['en'][:50]}"
    )
    review = Review(
        message=translations["original"],
        message_en=translations["en"],
        message_fr=translations["fr"],
        message_de=translations["de"],
        name=name,
        organisation=organisation,
        project_id=project_id,
        positive_message=positive_message,
        date=datetime.now().strftime("%d-%m-%y %H:%M:%S"),
    )
    db_session.add(review)
    db_session.commit()
    return review.id
