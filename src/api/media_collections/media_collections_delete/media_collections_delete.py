from fastapi import APIRouter, HTTPException, Request, Security
from fastapi.responses import JSONResponse
import logging
from src.shared.constants import STATUS_OK, STATUS_BAD_REQUEST
from src.entities.media_collections.media_collections import MediaCollections
from src.api.media_collections.media_collections_delete.docs import (
    summary_media_collections_delete,
    description_media_collections_delete,
    response_description_media_collections_delete,
)
from src.shared.db_config import DatabaseConnection
from src.shared.decorators.api_key_guard import require_api_key
from fastapi.security import APIKeyHeader
import os


router = APIRouter()
logger = logging.getLogger(__name__)

API_KEY_NAME = os.getenv("API_KEY_NAME")
api_key_header = APIKeyHeader(name=API_KEY_NAME)


@router.delete(
    "/{media_id}",
    summary=summary_media_collections_delete,
    description=description_media_collections_delete,
    response_description=response_description_media_collections_delete,
)
@require_api_key
async def media_collections_delete(
    media_id: int, request: Request, _: str = Security(api_key_header)
):
    try:
        logger.info(
            f"Received media_collections_delete request for media_id: {media_id}"
        )
        conn = DatabaseConnection()
        media = MediaCollections(conn)

        status, response = media.delete_media(media_id=media_id)
        if status != STATUS_OK:
            return JSONResponse(status_code=status, content=response)

        logger.info("Media deleted successfully.")
        return JSONResponse(status_code=200, content=response)

    except Exception as e:
        logger.error(f"Error in MediaCollectionsDelete: {e}")
        raise HTTPException(
            status_code=STATUS_BAD_REQUEST, detail=f"Media deletion failed: {e}"
        )
