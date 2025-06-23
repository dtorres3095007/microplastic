from pydantic import BaseModel
from typing import Optional
from fastapi import Form


class ForumPostForm(BaseModel):
    content: str
    author_name: Optional[str]

    @classmethod
    def as_form(
        cls,
        content: str = Form(..., description="Content of the forum post"),
        author_name: Optional[str] = Form(
            None, description="Name of the author of the post"
        ),
    ):
        return cls(
            content=content,
            author_name=author_name,
        )
