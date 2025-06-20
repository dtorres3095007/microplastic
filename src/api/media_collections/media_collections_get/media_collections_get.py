from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
import logging
from src.shared.constants import STATUS_OK, STATUS_BAD_REQUEST, STATUS_NOT_FOUND
from src.entities.media_collections.media_collections import MediaCollections
from src.api.media_collections.media_collections_get.docs import (
    summary_media_collections_get,
    description_media_collections_get,
    response_description_media_collections_get,
)
from src.shared.db_config import DatabaseConnection
from src.api.media_collections.media_collections_get.schema import MediaDetailsResponse


router = APIRouter()
logger = logging.getLogger(__name__)

@router.get(
    "/{media_id}",
    summary=summary_media_collections_get,
    description=description_media_collections_get,
    response_description=response_description_media_collections_get,
    response_model=MediaDetailsResponse,
    status_code=STATUS_OK,
)
async def media_collections_get(media_id: int):
    try:
        logger.info(f"Received media_collections_get request for media_id: {media_id}")
        conn = DatabaseConnection()
        media = MediaCollections(conn)

        status, media_details = media.get_media(media_id=media_id)
        if status != STATUS_OK:
            return  JSONResponse(
                status_code=STATUS_NOT_FOUND,
                content=media_details,
            )
        logger.info("Media retrieved successfully.")
        return MediaDetailsResponse(**media_details[0])

    except Exception as e:
        logger.error(f"Error in MediaCollectionsGet: {e}")
        raise HTTPException(status_code=STATUS_BAD_REQUEST, detail=f"Media retrieval failed: {e}")
    