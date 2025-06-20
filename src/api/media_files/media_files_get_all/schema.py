from pydantic import BaseModel, validator
import os
from typing import Optional


BASE_URL = os.getenv("MEDIA_BASE_URL")

class MediaFileOut(BaseModel):
    id: int
    collection_id: int
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
