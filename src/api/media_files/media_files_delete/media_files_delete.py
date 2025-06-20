from fastapi import APIRouter, HTTPException
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
import os


router = APIRouter()
logger = logging.getLogger(__name__)

MEDIA_DIR = "media/media_files"

@router.delete(
    "/{id}",
    summary=summary_media_files_delete,
    description=description_media_files_delete,
    response_description=response_description_media_files_delete
)
async def media_files_delete(id: int):
    try:
        conn = DatabaseConnection()
        logger.info(f"Received media_files_delete request for ID: {id}")
        media_files = MediaFiles(conn)

        status, message = media_files.get_media_file(id=id)
        if status != STATUS_OK:
            logger.error(f"Media file not found for ID: {id}")
            return JSONResponse(status_code=status, content=message)

        file_path = message[0]['url'].replace("/media/media_files/", MEDIA_DIR + "/")
        if os.path.exists(file_path):
            os.remove(file_path)
            logger.info(f"File {file_path} removed successfully.")
        else:
            logger.warning(f"File {file_path} does not exist, skipping removal.")
        
        status, message = media_files.delete_media_file(id=id)
        
        if status != STATUS_OK:
            return JSONResponse(status_code=status, content=message)
        
        logger.info(f"Media file deleted successfully for ID: {id}")
        return JSONResponse(status_code=200, content=message)

    except Exception as e:
        logger.error(f"Error in media_files_delete for ID {id}: {e}")
        raise HTTPException(status_code=STATUS_BAD_REQUEST, detail=f"Error deleting media file: {e}")
    