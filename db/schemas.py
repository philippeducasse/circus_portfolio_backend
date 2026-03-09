from pydantic import BaseModel
from typing import Optional


class ReviewCreate(BaseModel):
    message: str
    name: Optional[str] = "Anonymous"
    organisation: Optional[str] = None
    project_id: Optional[int] = None


class ReviewOut(BaseModel):
    id: int
    name: Optional[str]
    organisation: Optional[str]
    project_id: Optional[int]
    message: str
    message_en: Optional[str]
    message_fr: Optional[str]
    sentiment: Optional[str]
    date: str

    class Config:
        from_attributes = True