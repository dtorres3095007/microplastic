from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ForumGetAllQueryParams(BaseModel):
    limit: int = Field(
        default=10,
        gt=0,
        description="Maximum number of posts to return (default is 10, minimum is 1).",
    )
    offset: int = Field(
        default=0,
        ge=0,
        description="Number of posts to skip before starting to return results (default is 0, minimum is 0).",
    )
    search: Optional[str] = Field(
        default=None, description="Optional search term to filter posts by content."
    )


class ForumGetAllResponse(BaseModel):
    comment_id: int
    content: str
    author_name: Optional[str]
    created_at: datetime
