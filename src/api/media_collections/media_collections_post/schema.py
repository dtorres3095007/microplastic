from pydantic import BaseModel
from typing import Optional
from datetime import date
from fastapi import UploadFile, Form, File


class MediaCollectionRequestBody(BaseModel):
    title: str
    summary: str
    content: str
    media_type: str
    file: UploadFile
    thumbnail_url: Optional[UploadFile]
    published_at: date
    status: str

    @classmethod
    def as_form(
        cls,
        title: str = Form(..., description="Title of the media collection"),
        summary: str = Form(..., description="Summary of the media collection"),
        content: str = Form(..., description="Content of the media collection"),
        media_type: str = Form(
            ..., description="Type of the media collection (image, video, word, pdf)"
        ),
        file: UploadFile = File(..., description="Media file to be uploaded"),
        thumbnail_url: Optional[UploadFile] = File(
            None, description="Optional thumbnail image for the media collection"
        ),
        published_at: date = Form(
            ..., description="Date when the media collection was published"
        ),
        status: str = Form(
            ...,
            description="Status of the media collection (draft, published, archived)",
        ),
    ):
        return cls(
            title=title,
            summary=summary,
            content=content,
            media_type=media_type,
            file=file,
            thumbnail_url=thumbnail_url,
            published_at=published_at,
            status=status,
        )
