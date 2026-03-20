import logging

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from db.database import engine, get_db
from db.models import Base, Review
from db.schemas import ReviewCreate, ReviewOut
from jobs.jobs import review_processing_job

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


@app.post("/api/reviews")
def create_review(body: ReviewCreate, db: Session = Depends(get_db)):
    review_processing_job.execute_in_process(
        input_values={
            "message": body.message,
            "name": body.name,
            "organisation": body.organisation,
            "project_id": body.project_id,
            "db_session": db,
        }
    )

    review = db.query(Review).order_by(Review.id.desc()).first()
    return {"success": True, "id": review.id}


@app.get("/api/reviews", response_model=list[ReviewOut])
def get_reviews(db: Session = Depends(get_db)):
    return db.query(Review).filter(Review.positive_message).order_by(Review.date.desc())
