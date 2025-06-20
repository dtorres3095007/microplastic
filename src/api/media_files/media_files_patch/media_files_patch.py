from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from fastapi.responses import JSONResponse
import logging
import os
import uuid
from src.shared.constants import STATUS_OK, STATUS_BAD_REQUEST
from src.entities.media_files.media_files import MediaFiles
from src.api.media_files.media_files_patch.docs import (
    summary_media_files_patch,
    description_media_files_patch,
    response_description_media_files_patch,
)
from src.shared.db_config import DatabaseConnection


router = APIRouter()
logger = logging.getLogger(__name__)

@router.patch(
    "/{id}",
    summary=summary_media_files_patch,
    description=description_media_files_patch,
    response_description=response_description_media_files_patch
)
async def media_files_patch(
    id: int,
    type: str = Form(None, description="Type of the media file (e.g., image, video)"),
    title: str = Form(None, description="Title of the media file"),
    thumbnail_url: str = Form(None, description="URL of the thumbnail for the media file"),
    description: str = Form(None, description="Description of the media file"),
    file: UploadFile = File(None, description="Media file to be uploaded")
):
    try:
        conn = DatabaseConnection()
        logger.info(f"Received media_files_patch request with id {id}")
        media_files = MediaFiles(conn)
            
        status, message = media_files.update_media_file(
            id=id,
            type=type,
            title=title,
            file_content=await file.read() if file else None,
            original_filename=file.filename if file else None,
            thumbnail_url=thumbnail_url,
            description=description
        )

        if status == STATUS_OK:
            return JSONResponse(status_code=status, content=message)
        else:
            raise HTTPException(status_code=status, detail=message)

    except Exception as e:
        logger.error(f"Error updating media file with ID {id}: {e}")
        raise HTTPException(status_code=STATUS_BAD_REQUEST, detail="Error updating media file")
