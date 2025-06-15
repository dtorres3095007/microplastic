from pydantic import BaseModel, Field


class UserRequestBody(BaseModel):
    email: str = Field(..., example="johndoe", description="email of the user")
    password: str = Field(..., example="securepassword", description="Password of the user")

class UserPatchRequestBody(BaseModel):
    email: str = Field(None, example="johndoe", description="email of the user")
    profile: str = Field(..., example="normal", description="Profile of the user")
    active: bool = Field(..., example="1", description="Active status of the user")
    