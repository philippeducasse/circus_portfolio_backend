from typing import Optional

from dagster import job

from jobs.ops import save_review_op, sentiment_op, translate_op


@job
def review_processing_job(
    message: str,
    name: Optional[str],
    organisation: Optional[str],
    project_id: Optional[int],
    db_session,
):
    translations = translate_op(message)
    sentiment = sentiment_op(translations)
    save_review_op(translations, sentiment, db_session, name, organisation, project_id)
