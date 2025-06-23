from pydantic import BaseModel, Field, validator
from datetime import date
from typing import Optional
import os


BASE_URL = os.getenv("MEDIA_BASE_URL")


class MediaDetailsResponse(BaseModel):
    id: int
    title: str
    summary: str
    content: str
    media_type: str
    media_url: str
    thumbnail_url: Optional[str]
    published_at: Optional[date]
    status: str

    @validator("media_url", "thumbnail_url", pre=True, always=True)
    def add_base_url(cls, v):
        if v:
            return f"{BASE_URL}{v}" if not v.startswith("http") else v
        return v


class MediaCollectionsRequest(BaseModel):
    limit: int = Field(
        default=10,
        gt=0,
        description="Maximum number of media collections to return",
    )
    offset: int = Field(
        default=0,
        ge=0,
        description="Number of media collections to skip before starting to collect the result set",
    )
    search: Optional[str] = Field(
        default=None,
        description="Search term to filter media collections by title or description",
    )
