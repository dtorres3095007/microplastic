from fastapi import APIRouter, HTTPException, Depends, Request, Security
from fastapi.responses import JSONResponse
import logging
from src.shared.constants import STATUS_OK, STATUS_BAD_REQUEST
from src.entities.media_collections.media_collections import MediaCollections
from src.api.media_collections.media_collections_patch.schema import (
    MediaCollectionRequestBody,
)
from src.api.media_collections.media_collections_patch.docs import (
    summary_media_collections_patch,
    description_media_collections_patch,
    response_description_media_collections_patch,
)
from src.shared.db_config import DatabaseConnection
from src.shared.decorators.api_key_guard import require_api_key
from fastapi.security import APIKeyHeader
import os


router = APIRouter()
logger = logging.getLogger(__name__)

API_KEY_NAME = os.getenv("API_KEY_NAME")
api_key_header = APIKeyHeader(name=API_KEY_NAME)


@router.patch(
    "/{media_id}",
    summary=summary_media_collections_patch,
    description=description_media_collections_patch,
    response_description=response_description_media_collections_patch,
)
@require_api_key
async def media_collections_patch(
    media_id: int,
    request: Request,
    form: MediaCollectionRequestBody = Depends(MediaCollectionRequestBody.as_form),
    _: str = Security(api_key_header),
):
    try:
        logger.info(f"Received media_collections_patch request with data: {form}")
        conn = DatabaseConnection()
        media = MediaCollections(conn)

        status, message = media.update_media(
            media_id=media_id,
            title=form.title,
            summary=form.summary,
            content=form.content,
            media_type=form.media_type,
            file_content=await form.file.read() if form.file else None,
            original_filename=form.file.filename if form.file else None,
            thumbnail_content=(
                await form.thumbnail_url.read() if form.thumbnail_url else None
            ),
            thumbnail_filename=(
                form.thumbnail_url.filename if form.thumbnail_url else None
            ),
            published_at=form.published_at,
            status=form.status,
        )

        if status != STATUS_OK:
            return JSONResponse(status_code=status, content=message)

        logger.info("Media updated successfully.")
        return JSONResponse(status_code=200, content=message)

    except Exception as e:
        logger.error(f"Error in patch MediaCollectionsPatch: {e}")
        raise HTTPException(
            status_code=STATUS_BAD_REQUEST,
            detail=f"Media update failed: {e}",
        )
