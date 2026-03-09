import logging
from datetime import datetime
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from db.database import engine, get_db
from db.models import Base, Review
from db.schemas import ReviewCreate, ReviewOut
from services.llm import get_sentiment, translate_message, detect_language

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

    detect = await detect_language(body.message)
    print("detected", detect)

    translated_message = await translate_message(body.message)
    print("translated", translated_message)
    positive_message = None
    try:
        score = await get_sentiment(body.message)
        if score < 0.9:
            positive_message = False
        else:
            positive_message = True

    except Exception as e:
        logger.warning("Sentiment analysis failed: %s", e)

    review = Review(
        message=body.message,
        name=body.name,
        organisation=body.organisation,
        project_id=body.project_id,
        positive_message=positive_message,
        date=datetime.now().strftime("%d-%m-%y %H:%M:%S"),
    )
    db.add(review)
    db.commit()
    db.refresh(review)
    return {"success": True, "id": review.id}


@app.get("/reviews", response_model=list[ReviewOut])
def get_reviews(db: Session = Depends(get_db)):
    return db.query(Review).filter(Review.positive_message).order_by(Review.date.desc())
