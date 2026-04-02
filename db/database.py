from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import os

# Create SQLalchemy connection to the db
# FastAPI may check access db from different threads, so this is required
db_path = os.environ.get("DATABASE_URL", "sqlite:///portfolio.db")
engine = create_engine(db_path, connect_args={"check_same_thread": False})
# factory for creating database sessions. Each session is one unit of work with the DB -> tracks and flushes changes together
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Base call all ORMs inherit from.
Base = declarative_base()


def get_db():
    db = SessionLocal()   # open session before the route runs
    try:
        yield db          # hand the session to the route handler
    finally:
        db.close()        # always close it after, even if an exception occurred
