from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
import logging
from src.shared.constants import STATUS_OK, STATUS_BAD_REQUEST
from src.api.users.docs.get_docs import (
    summary_users_get,
    description_users_get,
    response_description_users_get,
)
from src.shared.db_config import DatabaseConnection
from src.entities.users.users import Users


router = APIRouter()
logger = logging.getLogger(__name__)

@router.get(
    "/",
    summary=summary_users_get,
    description=description_users_get,
    response_description=response_description_users_get
)

async def users_get():
    try:
        logger.info("Received users_get request")
        conn = DatabaseConnection()
        user = Users(conn)

        status, message = user.get_users()

        if status != STATUS_OK:
            return JSONResponse(
                status_code=status,
                content={"message": message['message']}
            )

        return JSONResponse(
            status_code=STATUS_OK,
            content=message
        )

    except Exception as e:
        logger.error(f"Error in get UsersGet: {e}")
        raise HTTPException(status_code=STATUS_BAD_REQUEST, detail=f"Get failed: {e}")
    