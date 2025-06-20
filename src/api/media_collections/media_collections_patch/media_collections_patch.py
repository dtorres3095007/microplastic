from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
import logging
from src.shared.constants import STATUS_OK, STATUS_BAD_REQUEST
from src.entities.media_collections.media_collections import MediaCollections
from src.api.media_collections.media_collections_patch.schema import MediaCollectionRequestBody
from src.api.media_collections.media_collections_patch.docs import (
    summary_media_collections_patch,
    description_media_collections_patch,
    response_description_media_collections_patch,
)
from src.shared.db_config import DatabaseConnection


router = APIRouter()
logger = logging.getLogger(__name__)

@router.patch(
    "/{media_id}",
    summary=summary_media_collections_patch,
    description=description_media_collections_patch,
    response_description=response_description_media_collections_patch
)
async def media_collections_patch(media_id: int, data: MediaCollectionRequestBody):
    try:
        logger.info(f"Received media_collections_patch request with data: {data}")
        conn = DatabaseConnection()
        media = MediaCollections(conn)

        status, message = media.update_media(
            media_id=media_id,
            title=data.title,
            description=data.description,
            date=data.date
        )
        if status != STATUS_OK:
            return JSONResponse(status_code=status, content=message)
        logger.info("Media updated successfully.")
        return JSONResponse(status_code=200, content=message)

    except Exception as e:
        logger.error(f"Error in patch MediaCollectionsPatch: {e}")
        raise HTTPException(status_code=STATUS_BAD_REQUEST, detail=f"Media update failed: {e}")
    