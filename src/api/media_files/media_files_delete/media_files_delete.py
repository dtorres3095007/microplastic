from fastapi import APIRouter, HTTPException, Request, Security
from fastapi.responses import JSONResponse
import logging
from src.shared.constants import STATUS_OK, STATUS_BAD_REQUEST
from src.entities.media_files.media_files import MediaFiles
from src.api.media_files.media_files_delete.docs import (
    summary_media_files_delete,
    description_media_files_delete,
    response_description_media_files_delete,
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
    "/{id}",
    summary=summary_media_files_delete,
    description=description_media_files_delete,
    response_description=response_description_media_files_delete,
)
@require_api_key
async def media_files_delete(
    id: int, request: Request, _: str = Security(api_key_header)
):
    try:
        conn = DatabaseConnection()
        logger.info(f"Received media_files_delete request for ID: {id}")
        media_files = MediaFiles(conn)

        status, message = media_files.delete_media_file(id=id)

        if status != STATUS_OK:
            return JSONResponse(status_code=status, content=message)

        logger.info(f"Media file deleted successfully for ID: {id}")
        return JSONResponse(status_code=200, content=message)

    except Exception as e:
        logger.error(f"Error in media_files_delete for ID {id}: {e}")
        raise HTTPException(
            status_code=STATUS_BAD_REQUEST, detail=f"Error deleting media file: {e}"
        )
