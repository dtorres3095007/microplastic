from fastapi import APIRouter, HTTPException, Depends, Request, Security
from fastapi.responses import JSONResponse
import logging
from src.shared.constants import STATUS_OK, STATUS_BAD_REQUEST
from src.entities.media_files.media_files import MediaFiles
from src.api.media_files.media_files_patch.docs import (
    summary_media_files_patch,
    description_media_files_patch,
    response_description_media_files_patch,
)
from src.shared.db_config import DatabaseConnection
from src.api.media_files.media_files_patch.schema import MediaFilePatchForm
from src.shared.decorators.api_key_guard import require_api_key
from fastapi.security import APIKeyHeader
import os


router = APIRouter()
logger = logging.getLogger(__name__)

API_KEY_NAME = os.getenv("API_KEY_NAME")
api_key_header = APIKeyHeader(name=API_KEY_NAME)


@router.patch(
    "/{id}",
    summary=summary_media_files_patch,
    description=description_media_files_patch,
    response_description=response_description_media_files_patch,
)
@require_api_key
async def media_files_patch(
    id: int,
    request: Request,
    form: MediaFilePatchForm = Depends(MediaFilePatchForm.as_form),
    _: str = Security(api_key_header),
):
    try:
        conn = DatabaseConnection()
        logger.info(f"Received media_files_patch request with id {id}")
        media_files = MediaFiles(conn)

        status, message = media_files.update_media_file(
            id=id,
            type=form.type,
            title=form.title,
            file_content=await form.file.read() if form.file else None,
            original_filename=form.file.filename if form.file else None,
            thumbnail_content=(
                await form.thumbnail_url.read() if form.thumbnail_url else None
            ),
            thumbnail_filename=(
                form.thumbnail_url.filename if form.thumbnail_url else None
            ),
            description=form.description,
        )

        if status == STATUS_OK:
            return JSONResponse(status_code=status, content=message)
        else:
            raise HTTPException(status_code=status, detail=message)

    except Exception as e:
        logger.error(f"Error updating media file with ID {id}: {e}")
        raise HTTPException(
            status_code=STATUS_BAD_REQUEST, detail="Error updating media file"
        )
