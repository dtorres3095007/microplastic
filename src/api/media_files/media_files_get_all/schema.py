from pydantic import BaseModel, validator, Field
import os
from typing import Optional


BASE_URL = os.getenv("MEDIA_BASE_URL")


class MediaFileOut(BaseModel):
    id: int
    title: str
    type: str
    url: str
    thumbnail_url: Optional[str] = None
    description: Optional[str] = None

    @validator("url", "thumbnail_url", pre=True, always=True)
    def add_base_url(cls, v):
        if v:
            return f"{BASE_URL}{v}" if not v.startswith("http") else v
        return v


class MediaFilesQueryParams(BaseModel):
    limit: int = Field(
        default=10, gt=0, description="Maximum number of media files to return"
    )
    offset: int = Field(
        default=0,
        ge=0,
        description="Number of media files to skip before starting to collect the result set",
    )
    search: Optional[str] = Field(
        default=None,
        description="Search term to filter media files by title or description",
    )
