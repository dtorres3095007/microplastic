from fastapi import APIRouter, HTTPException, Request, Security
from fastapi.responses import JSONResponse
import logging
from src.shared.constants import STATUS_OK, STATUS_BAD_REQUEST
from src.entities.media_files.media_files import MediaFiles
from src.api.media_files.media_files_get.docs import (
    summary_media_files_get,
    description_media_files_get,
    response_description_media_files_get,
)
from src.shared.db_config import DatabaseConnection
import os
from src.api.media_files.media_files_get.schema import MediaFileOut
from src.shared.decorators.api_key_guard import require_api_key
from fastapi.security import APIKeyHeader


router = APIRouter()
logger = logging.getLogger(__name__)

BASE_URL = os.getenv("MEDIA_BASE_URL")
API_KEY_NAME = os.getenv("API_KEY_NAME")
api_key_header = APIKeyHeader(name=API_KEY_NAME)


@router.get(
    "/{id}",
    summary=summary_media_files_get,
    description=description_media_files_get,
    response_description=response_description_media_files_get,
    response_model=MediaFileOut,
)
@require_api_key
async def media_files_get(id: int, request: Request, _: str = Security(api_key_header)):
    try:
        conn = DatabaseConnection()
        logger.info(f"Received media_files_get request for ID: {id}")
        media_files = MediaFiles(conn)

        status, content = media_files.get_media_file(id=id)

        if status != STATUS_OK:
            return JSONResponse(status_code=status, content=content)

        logger.info(f"Media file retrieved successfully for ID: {id}")
        return MediaFileOut(**content[0])

    except Exception as e:
        logger.error(f"Error in media_files_get for ID {id}: {e}")
        raise HTTPException(
            status_code=STATUS_BAD_REQUEST, detail=f"Error retrieving media file: {e}"
        )
