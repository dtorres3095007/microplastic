from fastapi import APIRouter, HTTPException, Depends, Request, Security
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
from src.api.media_files.media_files_post.schema import MediaFilePostForm
from src.shared.decorators.api_key_guard import require_api_key
from fastapi.security import APIKeyHeader
import os


router = APIRouter()
logger = logging.getLogger(__name__)

API_KEY_NAME = os.getenv("API_KEY_NAME")
api_key_header = APIKeyHeader(name=API_KEY_NAME)


@router.post(
    "/create",
    summary=summary_media_files_post,
    description=description_media_files_post,
    response_description=response_description_media_files_post,
)
@require_api_key
async def media_files_post(
    request: Request,
    form: MediaFilePostForm = Depends(MediaFilePostForm.as_form),
    _: str = Security(api_key_header),
):
    try:
        logger.info(f"Received media_files_post request with data: {form}")
        conn = DatabaseConnection()
        media = MediaFiles(conn)

        status, message = media.insert_media_file(
            type=form.type,
            title=form.title,
            file_content=await form.file.read(),
            original_filename=form.file.filename,
            thumbnail_content=(
                await form.thumbnail_url.read() if form.thumbnail_url else None
            ),
            thumbnail_filename=(
                form.thumbnail_url.filename if form.thumbnail_url else None
            ),
            description=form.description,
        )

        if status != STATUS_OK:
            return JSONResponse(status_code=status, content=message)
        logger.info("Media file created successfully.")
        return JSONResponse(status_code=200, content=message)

    except Exception as e:
        logger.error(f"Error in post MediaFilesPost: {e}")
        raise HTTPException(
            status_code=STATUS_BAD_REQUEST, detail=f"Media file creation failed: {e}"
        )
