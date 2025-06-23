from pydantic import BaseModel
from fastapi import Form, UploadFile, File
from typing import Optional


class MediaFilePostForm(BaseModel):
    type: str
    title: str
    thumbnail_url: Optional[UploadFile]
    description: Optional[str]
    file: UploadFile

    @classmethod
    def as_form(
        cls,
        type: str = Form(..., description="Type of the media file (image, video)"),
        title: str = Form(..., description="Title of the media file"),
        thumbnail_url: Optional[UploadFile] = File(
            None, description="Thumbnail image file (optional, can be uploaded)"
        ),
        description: Optional[str] = Form(
            None, description="Description of the media file"
        ),
        file: UploadFile = File(..., description="Media file to be uploaded"),
    ):
        return cls(
            type=type,
            title=title,
            thumbnail_url=thumbnail_url,
            description=description,
            file=file,
        )
