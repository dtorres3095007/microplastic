from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
import logging
from src.shared.constants import STATUS_OK, STATUS_BAD_REQUEST
from src.entities.media_collections.media_collections import MediaCollections
from src.api.media_collections.schema import MediaCollectionRequestBody
from src.api.media_collections.docs.media_collections_post_docs import (
    summary_media_colllections_post,
    description_media_colllections_post,
    response_description_media_colllections_post,
)
from src.shared.db_config import DatabaseConnection


router = APIRouter()
logger = logging.getLogger(__name__)

@router.post(
    "/create",
    summary=summary_media_colllections_post,
    description=description_media_colllections_post,
    response_description=response_description_media_colllections_post
)
async def media_collections_post(data: MediaCollectionRequestBody):
    try:
        logger.info(f"Received media_collections_post request with data: {data}")
        conn = DatabaseConnection()
        media = MediaCollections(conn)

        status, message = media.insert_media(
            title=data.title,
            description=data.description,
            date=data.date
        )
        if status != STATUS_OK:
            return JSONResponse(status_code=status, content=message)
        logger.info("Media completed successfully.")
        return JSONResponse(status_code=200, content=message)

    except Exception as e:
        logger.error(f"Error in post MediaCollectionsPost: {e}")
        raise HTTPException(status_code=STATUS_BAD_REQUEST, detail=f"images download failed: {e}")
