from typing import Optional

from pydantic import BaseModel


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
    message_de: Optional[str]
    positive_message: Optional[bool]
    original_message_language: Optional[str]
    date: str

    class Config:
        from_attributes = True
