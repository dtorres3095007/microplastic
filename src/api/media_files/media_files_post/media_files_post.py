from fastapi import APIRouter, HTTPException, Form, UploadFile, File
from fastapi.responses import JSONResponse
import logging
from src.shared.constants import STATUS_OK, STATUS_BAD_REQUEST
from src.entities.media_files.media_files import MediaFiles
from src.api.media_files.media_files_post.docs import (
    summary_media_files_post,
    description_media_files_post,
    response_description_media_files_post,
)
from src.shared.db_config import DatabaseConnection
import uuid
import os


router = APIRouter()
logger = logging.getLogger(__name__)

MEDIA_DIR = "media/media_files"

@router.post(
    "/create",
    summary=summary_media_files_post,
    description=description_media_files_post,
    response_description=response_description_media_files_post
)
async def media_files_post(
    collection_id: str = Form(..., description="ID of the collection of the media file"),
    type: str = Form(..., description="Type of the media file (e.g., image, video)"),
    title: str = Form(..., description="Title of the media file"),
    file: UploadFile = File(..., description="Media file to be uploaded"),
    thumbnail_url: str = Form(None, description="URL of the thumbnail for the media file"),
    description: str = Form(None, description="Description of the media file"),):
    try:
        logger.info(f"Received media_files_post request with data: {title}")
        conn = DatabaseConnection()
        media = MediaFiles(conn)

        content = await file.read()

        status, message = media.insert_media_file(
            collection_id=collection_id,
            type=type,
            title=title,
            file_content=content,
            original_filename=file.filename,
            thumbnail_url=thumbnail_url,
            description=description
        )

        if status != STATUS_OK:
            return JSONResponse(status_code=status, content=message)
        logger.info("Media file created successfully.")
        return JSONResponse(status_code=200, content=message)

    except Exception as e:
        logger.error(f"Error in post MediaFilesPost: {e}")
        raise HTTPException(status_code=STATUS_BAD_REQUEST, detail=f"Media file creation failed: {e}")
    