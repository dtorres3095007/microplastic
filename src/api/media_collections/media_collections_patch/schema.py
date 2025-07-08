from pydantic import BaseModel
from typing import Optional
from datetime import date
from fastapi import UploadFile, Form, File


class MediaCollectionRequestBody(BaseModel):
    title: Optional[str]
    summary: Optional[str]
    content: Optional[str]
    media_type: Optional[str]
    file: Optional[UploadFile]
    thumbnail_url: Optional[UploadFile]
    published_at: Optional[date]
    status: Optional[str]

    @classmethod
    def as_form(
        cls,
        title: Optional[str] = Form(None, description="Title of the media collection"),
        summary: Optional[str] = Form(
            None, description="Summary of the media collection"
        ),
        content: Optional[str] = Form(
            None, description="Content of the media collection"
        ),
        media_type: Optional[str] = Form(
            None, description="Type of the media collection (image, video, word, pdf)"
        ),
        file: Optional[UploadFile] = File(
            None, description="Media file to be uploaded"
        ),
        thumbnail_url: Optional[UploadFile] = File(
            None, description="Optional thumbnail image for the media collection"
        ),
        published_at: Optional[date] = Form(
            None, description="Date when the media collection was published"
        ),
        status: Optional[str] = Form(
            None,
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
