from pydantic import BaseModel, Field


class UserPatchRequestBody(BaseModel):
    email: str = Field(None, example="johndoe", description="email of the user")
    profile: str = Field(..., example="normal", description="Profile of the user")
    active: int = Field(..., example="1", description="Active status of the user")
    