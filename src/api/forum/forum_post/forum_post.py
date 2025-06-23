from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
import logging
from src.shared.constants import STATUS_OK, STATUS_BAD_REQUEST
from src.entities.forum.forum import Forum
from src.api.forum.forum_post.docs import (
    summary_forum_post,
    description_forum_post,
    response_description_forum_post,
)
from src.shared.db_config import DatabaseConnection
from src.api.forum.forum_post.schema import ForumPostForm


router = APIRouter()
logger = logging.getLogger(__name__)


@router.post(
    "/posts",
    summary=summary_forum_post,
    description=description_forum_post,
    response_description=response_description_forum_post,
)
async def forum_post(
    form: ForumPostForm = Depends(ForumPostForm.as_form),
):
    try:
        logger.info(f"Received forum_post request with data: {form}")
        conn = DatabaseConnection()
        forum = Forum(conn)

        status, message = forum.insert_forum_post(
            content=form.content,
            author_name=form.author_name,
        )

        if status != STATUS_OK:
            raise HTTPException(status_code=status, detail=message)

        logger.info("Forum post created successfully.")
        return JSONResponse(status_code=200, content=message)

    except Exception as e:
        logger.error(f"Error in post ForumPost: {e}")
        raise HTTPException(
            status_code=STATUS_BAD_REQUEST, detail=f"Forum post creation failed: {e}"
        )
