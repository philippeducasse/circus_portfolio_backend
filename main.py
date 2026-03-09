from datetime import datetime
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from db.database import engine, get_db
from db.models import Base, Review
from db.schemas import ReviewCreate, ReviewOut
from services.llm import get_sentiment

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
    try:
        await get_sentiment(body.message)
    except Exception:
        pass  

    review = Review(
        message=body.message,
        name=body.name,
        organisation=body.organisation,
        project_id=body.project_id,
        date=datetime.now().strftime("%d-%m-%y %H:%M:%S"),
    )
    db.add(review)
    db.commit()
    db.refresh(review)
    return {"success": True, "id": review.id}


@app.get("/reviews", response_model=list[ReviewOut])
def get_reviews(db: Session = Depends(get_db)):
    return db.query(Review).order_by(Review.date.desc()).all()