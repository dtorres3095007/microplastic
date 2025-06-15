from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
import logging
from src.shared.constants import STATUS_OK, STATUS_BAD_REQUEST
from src.entities.media_files.media_files import MediaFiles
from src.api.media_files.docs.media_files_get_docs import (
    summary_media_files_get,
    description_media_files_get,
    response_description_media_files_get,
)
from src.shared.db_config import DatabaseConnection
import os


router = APIRouter()
logger = logging.getLogger(__name__)
BASE_URL = os.getenv("MEDIA_BASE_URL")

@router.get(
    "/{id}",
    summary=summary_media_files_get,
    description=description_media_files_get,
    response_description=response_description_media_files_get
)
async def media_files_get(id: int):
    try:
        conn = DatabaseConnection()
        logger.info(f"Received media_files_get request for ID: {id}")
        media_files = MediaFiles(conn)
        
        status, message = media_files.get_media_file(id=id)
        
        if status != STATUS_OK:
            return JSONResponse(status_code=status, content=message)
        
        logger.info(f"Media file retrieved successfully for ID: {id}")
        if message[0]['url'] is not None:
            message[0]['url'] = f"{BASE_URL}{message[0]['url']}"
        return JSONResponse(status_code=200, content=message)

    except Exception as e:
        logger.error(f"Error in media_files_get for ID {id}: {e}")
        raise HTTPException(status_code=STATUS_BAD_REQUEST, detail=f"Error retrieving media file: {e}")
    