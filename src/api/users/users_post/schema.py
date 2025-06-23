from pydantic import BaseModel, Field


class UserRequestBody(BaseModel):
    email: str = Field(..., example="johndoe", description="email of the user")
    password: str = Field(
        ..., example="securepassword", description="Password of the user"
    )
    profile: str = Field(
        ...,
        example="normal",
        description="Profile of the user, can be 'normal' or 'admin'",
    )
