from datetime import datetime
from unittest.mock import patch, MagicMock

from db.models import Review


def make_review(db, positive=True, **kwargs):
    review = Review(
        message=kwargs.get("message", "Great work!"),
        message_en=kwargs.get("message_en", "Great work!"),
        message_fr=kwargs.get("message_fr", "Super travail!"),
        message_de=kwargs.get("message_de", "Tolle Arbeit!"),
        name=kwargs.get("name", "Test User"),
        organisation=kwargs.get("organisation", None),
        project_id=kwargs.get("project_id", None),
        positive_message=positive,
        date=datetime.now().strftime("%d-%m-%y %H:%M:%S"),
    )
    db.add(review)
    db.commit()
    db.refresh(review)
    return review


def mock_job_execution(db_session, translations, sentiment_score):
    """Simulate what the Dagster job does: save a review to the DB."""
    review = Review(
        message=translations["original"],
        message_en=translations["en"],
        message_fr=translations["fr"],
        message_de=translations["de"],
        positive_message=sentiment_score > 0.9,
        date=datetime.now().strftime("%d-%m-%y %H:%M:%S"),
    )
    db_session.add(review)
    db_session.commit()


class TestPostReview:
    def test_creates_review_and_returns_id(self, client, db_session):
        translations = {
            "original": "Great work!",
            "source_lang": "en",
            "en": "Great work!",
            "fr": "Super travail!",
            "de": "Tolle Arbeit!",
        }

        def fake_execute(input_values):
            mock_job_execution(db_session, translations, sentiment_score=0.95)

        with patch("main.review_processing_job.execute_in_process", side_effect=fake_execute):
            response = client.post("/reviews", json={"message": "Great work!"})

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert isinstance(data["id"], int)

    def test_accepts_optional_fields(self, client, db_session):
        translations = {
            "original": "Bon travail",
            "source_lang": "fr",
            "en": "Good work",
            "fr": "Bon travail",
            "de": "Gute Arbeit",
        }

        def fake_execute(input_values):
            mock_job_execution(db_session, translations, sentiment_score=0.95)

        payload = {
            "message": "Bon travail",
            "name": "Alice",
            "organisation": "Acme",
            "project_id": 42,
        }

        with patch("main.review_processing_job.execute_in_process", side_effect=fake_execute):
            response = client.post("/reviews", json=payload)

        assert response.status_code == 200
        assert response.json()["success"] is True

    def test_missing_message_returns_422(self, client):
        response = client.post("/reviews", json={"name": "Alice"})
        assert response.status_code == 422


class TestGetReviews:
    def test_returns_empty_list(self, client):
        response = client.get("/reviews")
        assert response.status_code == 200
        assert response.json() == []

    def test_returns_only_positive_reviews(self, client, db_session):
        make_review(db_session, positive=True, message="Loved it!")
        make_review(db_session, positive=False, message="Terrible.")

        response = client.get("/reviews")
        assert response.status_code == 200
        reviews = response.json()
        assert len(reviews) == 1
        assert reviews[0]["message"] == "Loved it!"

    def test_response_shape(self, client, db_session):
        make_review(db_session, positive=True, name="Bob", organisation="WidgetCo", project_id=1)

        response = client.get("/reviews")
        assert response.status_code == 200
        review = response.json()[0]

        for field in ("id", "name", "organisation", "project_id", "message", "date", "positive_message"):
            assert field in review

    def test_returns_multiple_positive_reviews(self, client, db_session):
        for i in range(3):
            make_review(db_session, positive=True, message=f"Great {i}")
        make_review(db_session, positive=False, message="Bad")

        response = client.get("/reviews")
        assert len(response.json()) == 3
