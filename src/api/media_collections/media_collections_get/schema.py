from pydantic import BaseModel, Field
from datetime import date


class MediaDetailsResponse(BaseModel):
    id: int
    title: str
    description: str
    date: date
    