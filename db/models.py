from sqlalchemy import Column, Integer, Text, Boolean
from db.database import Base


class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text)
    organisation = Column(Text)
    project_id = Column(Integer)
    message = Column(Text, nullable=False)
    message_en = Column(Text)
    message_fr = Column(Text)
    positive_message = Column(Boolean)
    date = Column(Text, nullable=False)
