from pydantic import BaseModel, Field
from typing import Optional


class UserGetAllQueryParams(BaseModel):
    limit: int = Field(
        default=10, gt=0, description="Maximum number of users to return"
    )
    offset: int = Field(
        default=0,
        ge=0,
        description="Number of users to skip before starting to collect the result set",
    )
    search: Optional[str] = Field(
        default=None, description="Search term to filter users by email"
    )
