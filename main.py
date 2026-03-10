import logging
from datetime import datetime

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from db.database import engine, get_db
from db.models import Base, Review
from db.schemas import ReviewCreate, ReviewOut
from services.llm import get_sentiment, translate_message

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://philippeducasse.com",
        "http://127.0.0.1:3000",
    ],
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type"],
)


@app.post("/reviews")
async def create_review(body: ReviewCreate, db: Session = Depends(get_db)):
    translations = await translate_message(body.message)

    positive_message = None
    try:
        score = await get_sentiment(translations["en"])
        logger.info("Sentiment score:", score)
        if score < 0.9:
            logger.info("received a negative review")
            positive_message = False
        else:
            logger.info("received a positive review")
            positive_message = True

    except Exception as e:
        logger.warning("Sentiment analysis failed: %s", e)

    review = Review(
        message=translations["original"],
        message_en=translations["en"],
        message_fr=translations["fr"],
        message_de=translations["de"],
        name=body.name,
        organisation=body.organisation,
        project_id=body.project_id,
        positive_message=positive_message,
        date=datetime.now().strftime("%d-%m-%y %H:%M:%S"),
    )
    db.add(review)
    db.commit()
    db.refresh(review)
    logger.info(f"Adding new review: {review.__dict__}")
    return {"success": True, "id": review.id}


@app.get("/reviews", response_model=list[ReviewOut])
def get_reviews(db: Session = Depends(get_db)):
    return db.query(Review).filter(Review.positive_message).order_by(Review.date.desc())
