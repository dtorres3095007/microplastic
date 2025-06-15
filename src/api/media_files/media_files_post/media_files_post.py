from fastapi import APIRouter, HTTPException, Form, UploadFile, File
from fastapi.responses import JSONResponse
import logging
from src.shared.constants import STATUS_OK, STATUS_BAD_REQUEST
from src.entities.media_files.media_files import MediaFiles
from src.api.media_files.docs.media_files_post_docs import (
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
    collection_id: str = Form(...),
    type: str = Form(...),
    title: str = Form(...),
    file: UploadFile = File(...),
    thumbnail_url: str = Form(None),
    description: str = Form(None),):
    try:
        logger.info(f"Received media_files_post request with data: {title}")
        conn = DatabaseConnection()
        media = MediaFiles(conn)

        # Create a unique filename for the uploaded file
        extension = os.path.splitext(file.filename)[1]
        unique_name = f"{uuid.uuid4().hex}{extension}"
        file_path = os.path.join(MEDIA_DIR, unique_name)

        # Save the uploaded file
        os.makedirs(MEDIA_DIR, exist_ok=True)
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)

        # Generate URL for the media file
        url = f"/media/media_files/{unique_name}"

        status, message = media.insert_media_file(
            collection_id=collection_id,
            type=type,
            title=title,
            url=url,
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
    