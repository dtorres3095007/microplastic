from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
import logging
from src.shared.constants import STATUS_OK, STATUS_BAD_REQUEST
from src.api.users.users_get.docs import (
    summary_user_get,
    description_user_get,
    response_description_user_get,
)
from src.shared.db_config import DatabaseConnection
from src.entities.users.users import Users


router = APIRouter()
logger = logging.getLogger(__name__)


@router.get(
    "/{user_id}",
    summary=summary_user_get,
    description=description_user_get,
    response_description=response_description_user_get,
)
async def user_get(user_id: int):
    try:
        logger.info("Received user_get request")
        conn = DatabaseConnection()
        user = Users(conn)

        status, message = user.get_user_by_id(user_id=user_id)

        if status != STATUS_OK:
            return JSONResponse(
                status_code=status, content={"message": message["message"]}
            )

        return JSONResponse(status_code=STATUS_OK, content=message)

    except Exception as e:
        logger.error(f"Error in get UserGet: {e}")
        raise HTTPException(status_code=STATUS_BAD_REQUEST, detail=f"Get failed: {e}")
