from pydantic import BaseModel
from typing import Optional


class ForumPostForm(BaseModel):
    content: str
    author_name: Optional[str]
