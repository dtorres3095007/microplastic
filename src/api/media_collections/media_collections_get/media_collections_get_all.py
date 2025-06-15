from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
import logging
from src.shared.constants import STATUS_OK, STATUS_BAD_REQUEST
from src.entities.media_collections.media_collections import MediaCollections
from src.api.media_collections.docs.media_collections_get_all_docs import (
    summary_media_colllections_get_all,
    description_media_colllections_get_all,
    response_description_media_colllections_get_all,
)
from src.shared.db_config import DatabaseConnection
from src.api.media_collections.schema import MediaDetailsResponse
from typing import List


router = APIRouter()
logger = logging.getLogger(__name__)

@router.get(
    "/",
    summary=summary_media_colllections_get_all,
    description=description_media_colllections_get_all,
    response_description=response_description_media_colllections_get_all,
    response_model=List[MediaDetailsResponse],
    status_code=STATUS_OK,
)
async def media_collections_get_all():
    try:
        logger.info("Received media_collections_get_all request")
        conn = DatabaseConnection()
        media = MediaCollections(conn)

        status, all_media = media.get_all_media()
        if status != STATUS_OK:
            return JSONResponse(status_code=status, content=all_media)
        
        logger.info("All media retrieved successfully.")
        return [MediaDetailsResponse(**item) for item in all_media]

    except Exception as e:
        logger.error(f"Error in MediaCollectionsGetAll: {e}")
        raise HTTPException(status_code=STATUS_BAD_REQUEST, detail=f"Media retrieval failed: {e}")
    