from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from fastapi.responses import JSONResponse
import logging
import os
import uuid
from src.shared.constants import STATUS_OK, STATUS_BAD_REQUEST
from src.entities.media_files.media_files import MediaFiles
from src.api.media_files.docs.media_files_patch_docs import (
    summary_media_files_patch,
    description_media_files_patch,
    response_description_media_files_patch,
)
from src.shared.db_config import DatabaseConnection


router = APIRouter()
logger = logging.getLogger(__name__)

MEDIA_DIR = "media/media_files"

@router.patch(
    "/{id}",
    summary=summary_media_files_patch,
    description=description_media_files_patch,
    response_description=response_description_media_files_patch
)
async def media_files_patch(
    id: int,
    type: str = Form(None),
    title: str = Form(None),
    thumbnail_url: str = Form(None),
    description: str = Form(None),
    file: UploadFile = File(None)
):
    try:
        conn = DatabaseConnection()
        logger.info(f"Received media_files_patch request with id {id}")
        media_files = MediaFiles(conn)

        new_url = None
        if file:
            # Create a unique filename for the uploaded file
            extension = os.path.splitext(file.filename)[1]
            unique_name = f"{uuid.uuid4().hex}{extension}"
            file_path = os.path.join(MEDIA_DIR, unique_name)

            # Save the uploaded file
            os.makedirs(MEDIA_DIR, exist_ok=True)
            with open(file_path, "wb") as f:
                f.write(await file.read())

            # Generate URL for the media file
            new_url = f"/media/media_files/{unique_name}"

            status_code, message = media_files.get_media_file(id=id)
            if status_code != STATUS_OK:
                return HTTPException(status_code=STATUS_BAD_REQUEST, detail=message)
            os.remove(message[0]['url'].replace("/media/media_files/", MEDIA_DIR + "/"))
            
        status, message = media_files.update_media_file(
            id=id,
            type=type,
            title=title,
            url=new_url,
            thumbnail_url=thumbnail_url,
            description=description
        )

        if status == STATUS_OK:
            return JSONResponse(status_code=status, content={"message": message})
        else:
            raise HTTPException(status_code=status, detail=message)

    except Exception as e:
        logger.error(f"Error updating media file with ID {id}: {e}")
        raise HTTPException(status_code=STATUS_BAD_REQUEST, detail="Error updating media file")
