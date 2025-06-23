from fastapi import APIRouter, HTTPException, Depends
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
from typing import List
from src.api.media_files.media_files_get_all.schema import (
    MediaFileOut,
    MediaFilesQueryParams,
)


router = APIRouter()
logger = logging.getLogger(__name__)


@router.get(
    "/",
    summary=summary_media_files_get_all,
    description=description_media_files_get_all,
    response_description=response_description_media_files_get_all,
    response_model=List[MediaFileOut],
)
async def media_files_get_all(
    query: MediaFilesQueryParams = Depends(),
):
    try:
        conn = DatabaseConnection()
        logger.info("Received media_files_get_all request")
        media_files = MediaFiles(conn)

        status, data = media_files.get_all_media_files(
            limit=query.limit,
            offset=query.offset,
            search=query.search,
        )

        if status != STATUS_OK:
            return JSONResponse(status_code=status, content=data)

        logger.info("Media files retrieved successfully")
        return data

    except Exception as e:
        logger.error(f"Error in media_files_get_all: {e}")
        raise HTTPException(
            status_code=STATUS_BAD_REQUEST, detail=f"Error retrieving media files: {e}"
        )
