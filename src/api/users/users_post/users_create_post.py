from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
import logging
from src.shared.constants import STATUS_OK, STATUS_BAD_REQUEST
from src.api.users.users_post.docs import (
    summary_create,
    description_create,
    response_description_create,
)
from src.api.users.users_post.schema import UserRequestBody
from src.shared.db_config import DatabaseConnection
from src.entities.users.users import Users


router = APIRouter()
logger = logging.getLogger(__name__)

@router.post(
    "/create",
    summary=summary_create,
    description=description_create,
    response_description=response_description_create
)
async def users_create_post(data: UserRequestBody):
    try:
        logger.info(f"Received users_create_post request with data: {data}")
        conn = DatabaseConnection()
        user = Users(conn)

        status, message =user.create_user(
            email=data.email,
            password=data.password,
            profile=data.profile
        )

        if status != STATUS_OK:
            return JSONResponse(
                status_code=status,
                content={"message": message['message']}
            )

    except Exception as e:
        logger.error(f"Error in post UsersCreatePost: {e}")
        raise HTTPException(status_code=STATUS_BAD_REQUEST, detail=f"Create failed: {e}" )
    