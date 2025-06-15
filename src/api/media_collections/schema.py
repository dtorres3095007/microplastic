from pydantic import BaseModel, Field
from datetime import date


class MediaCollectionRequestBody(BaseModel):
    title: str = Field(..., example="My Collection", description="Title of the media collection")
    description: str = Field(None, example="A collection of my favorite media", description="Description of the media collection")
    date: date

class MediaDetailsResponse(BaseModel):
    id: int
    title: str
    description: str
    date: date
    