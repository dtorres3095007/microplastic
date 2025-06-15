from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
import logging
from src.shared.constants import STATUS_OK, STATUS_BAD_REQUEST
from src.entities.media_files.media_files import MediaFiles
from src.api.media_files.docs.media_files_get_docs import (
    summary_media_files_get_all,
    description_media_files_get_all,
    response_description_media_files_get_all,
)
from src.shared.db_config import DatabaseConnection
import os


router = APIRouter()
logger = logging.getLogger(__name__)
BASE_URL = os.getenv("MEDIA_BASE_URL")

@router.get(
    "/collection/{collection_id}",
    summary=summary_media_files_get_all,
    description=description_media_files_get_all,
    response_description=response_description_media_files_get_all
)
async def media_files_get_all(collection_id: int):
    try:
        conn = DatabaseConnection()
        logger.info("Received media_files_get_all request")
        media_files = MediaFiles(conn)
        
        status, message = media_files.get_all_media_files(collection_id=collection_id)
        
        if status != STATUS_OK:
            return JSONResponse(status_code=status, content=message)
        
        logger.info("Media files retrieved successfully")
        for message_item in message:
            if 'url' in message_item:
                message_item['url'] = f"{BASE_URL}{message_item['url']}"
            if 'thumbnail_url' in message_item and message_item['thumbnail_url']:
                message_item['thumbnail_url'] = f"{BASE_URL}{message_item['thumbnail_url']}"

        return JSONResponse(status_code=200, content=message)

    except Exception as e:
        logger.error(f"Error in media_files_get_all: {e}")
        raise HTTPException(status_code=STATUS_BAD_REQUEST, detail=f"Error retrieving media files: {e}")
    