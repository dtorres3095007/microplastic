from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
import logging
from src.shared.constants import STATUS_OK, STATUS_BAD_REQUEST
from src.entities.media_files.media_files import MediaFiles
from src.api.media_files.media_files_get_all.docs import (
    summary_media_files_get_all,
    description_media_files_get_all,
    response_description_media_files_get_all,
)
from src.shared.db_config import DatabaseConnection
import os
from typing import List
from src.api.media_files.media_files_get_all.schema import MediaFileOut
from fastapi import Query


router = APIRouter()
logger = logging.getLogger(__name__)

@router.get(
    "/collection/{collection_id}",
    summary=summary_media_files_get_all,
    description=description_media_files_get_all,
    response_description=response_description_media_files_get_all,
    response_model=List[MediaFileOut]
)
async def media_files_get_all(
    collection_id: int,
    limit: int = Query(10, gt=0, description="Maximum number of media files to return"),
    offset: int = Query(0, ge=0, description="Number of media files to skip before starting to collect the result set"),
    search: str = Query(None, description="Search term to filter media files by title or description")
    ):
    try:
        conn = DatabaseConnection()
        logger.info("Received media_files_get_all request")
        media_files = MediaFiles(conn)
        
        status, data = media_files.get_all_media_files(
            collection_id=collection_id,
            limit=limit,
            offset=offset,
            search=search
            )
        
        if status != STATUS_OK:
            return JSONResponse(status_code=status, content=data)
        
        logger.info("Media files retrieved successfully")
        return data

    except Exception as e:
        logger.error(f"Error in media_files_get_all: {e}")
        raise HTTPException(status_code=STATUS_BAD_REQUEST, detail=f"Error retrieving media files: {e}")
    