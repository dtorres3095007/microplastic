from fastapi import APIRouter, HTTPException, Depends, Request, Security
from fastapi.responses import JSONResponse
import logging
from src.shared.constants import STATUS_OK, STATUS_BAD_REQUEST
from src.entities.media_collections.media_collections import MediaCollections
from src.api.media_collections.media_collections_get_all.docs import (
    summary_media_collections_get_all,
    description_media_collections_get_all,
    response_description_media_collections_get_all,
)
from src.shared.db_config import DatabaseConnection
from src.api.media_collections.media_collections_get_all.schema import (
    MediaDetailsResponse,
    MediaCollectionsRequest,
)
from typing import List
from src.shared.decorators.api_key_guard import require_api_key
from fastapi.security import APIKeyHeader
import os


router = APIRouter()
logger = logging.getLogger(__name__)

API_KEY_NAME = os.getenv("API_KEY_NAME")
api_key_header = APIKeyHeader(name=API_KEY_NAME)


@router.get(
    "/",
    summary=summary_media_collections_get_all,
    description=description_media_collections_get_all,
    response_description=response_description_media_collections_get_all,
    response_model=List[MediaDetailsResponse],
    status_code=STATUS_OK,
)
@require_api_key
async def media_collections_get_all(
    request: Request,
    query: MediaCollectionsRequest = Depends(),
    _: str = Security(api_key_header),
):
    try:
        logger.info("Received media_collections_get_all request")
        conn = DatabaseConnection()
        media = MediaCollections(conn)

        status, all_media = media.get_all_media(
            limit=query.limit, offset=query.offset, search=query.search
        )
        if status != STATUS_OK:
            return JSONResponse(status_code=status, content=all_media)

        logger.info("All media retrieved successfully.")
        return all_media

    except Exception as e:
        logger.error(f"Error in MediaCollectionsGetAll: {e}")
        raise HTTPException(
            status_code=STATUS_BAD_REQUEST, detail=f"Media retrieval failed: {e}"
        )
