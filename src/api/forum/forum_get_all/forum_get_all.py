from fastapi import APIRouter, HTTPException, Depends, Request, Security
import logging
from src.shared.constants import STATUS_OK, STATUS_BAD_REQUEST
from src.api.forum.forum_get_all.docs import (
    summary_forum_get_all,
    description_forum_get_all,
    response_description_forum_get_all,
)
from src.shared.db_config import DatabaseConnection
from src.entities.forum.forum import Forum
from src.api.forum.forum_get_all.schema import (
    ForumGetAllQueryParams,
    ForumGetAllResponse,
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
    "/posts",
    summary=summary_forum_get_all,
    description=description_forum_get_all,
    response_description=response_description_forum_get_all,
    response_model=List[ForumGetAllResponse],
)
@require_api_key
async def forum_get_all(
    request: Request,
    query: ForumGetAllQueryParams = Depends(),
    _: str = Security(api_key_header),
):
    try:
        logger.info("Received forum_get_all request")
        conn = DatabaseConnection()
        forum = Forum(conn)

        status, message = forum.forum_get_all(
            limit=query.limit, offset=query.offset, search=query.search
        )

        if status != STATUS_OK:
            raise HTTPException(status_code=status, detail=message)

        return message

    except Exception as e:
        logger.error(f"Error in get ForumGetAll: {e}")
        raise HTTPException(status_code=STATUS_BAD_REQUEST, detail=f"Get failed: {e}")
