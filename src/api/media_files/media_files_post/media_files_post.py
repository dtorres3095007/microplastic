from fastapi import APIRouter, HTTPException, Depends
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


router = APIRouter()
logger = logging.getLogger(__name__)

MEDIA_DIR = "media/media_files"


@router.post(
    "/create",
    summary=summary_media_files_post,
    description=description_media_files_post,
    response_description=response_description_media_files_post,
)
async def media_files_post(
    form: MediaFilePostForm = Depends(MediaFilePostForm.as_form),
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
