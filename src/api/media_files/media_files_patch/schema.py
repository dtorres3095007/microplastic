from pydantic import BaseModel
from fastapi import Form, UploadFile, File
from typing import Optional


class MediaFilePatchForm(BaseModel):
    type: Optional[str]
    title: Optional[str]
    thumbnail_url: Optional[UploadFile]
    description: Optional[str]
    file: Optional[UploadFile]

    @classmethod
    def as_form(
        cls,
        type: Optional[str] = Form(
            None, description="Type of the media file (image, video)"
        ),
        title: Optional[str] = Form(None, description="Title of the media file"),
        thumbnail_url: Optional[UploadFile] = File(
            None, description="URL of the thumbnail for the media file"
        ),
        description: Optional[str] = Form(
            None, description="Description of the media file"
        ),
        file: Optional[UploadFile] = File(
            None, description="Media file to be uploaded"
        ),
    ):
        return cls(
            type=type,
            title=title,
            thumbnail_url=thumbnail_url,
            description=description,
            file=file,
        )
