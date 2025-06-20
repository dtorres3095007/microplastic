from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
import logging
from src.shared.constants import STATUS_OK, STATUS_BAD_REQUEST
from src.api.users.users_login_post.docs import (
    summary_login,
    description_login,
    response_description_login,
)
from src.api.users.users_login_post.schema import UserRequestBody
from src.shared.db_config import DatabaseConnection
from src.entities.users.users import Users
from src.shared.jwt_handler import create_access_token, create_refresh_token


router = APIRouter()
logger = logging.getLogger(__name__)

@router.post(
    "/login",
    summary=summary_login,
    description=description_login,
    response_description=response_description_login
)
async def users_login_post(data: UserRequestBody):
    try:
        logger.info(f"Received users_login_post request with data: {data}")
        conn = DatabaseConnection()
        user = Users(conn)

        status, message =user.login_user(
            email=data.email,
            password=data.password,
        )
        if status != STATUS_OK:
            return JSONResponse(
                status_code=status,
                content={"message": message['message']}
            )
        logger.info("User authenticated successfully.")
        access_token = create_access_token(data={"sub": message['user'][0]['email']})
        refresh_token = create_refresh_token(data={"sub": message['user'][0]['email']})
        return JSONResponse(
            status_code=200,
            content={"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}
        )

    except Exception as e:
        logger.error(f"Error in post UsersLoginPost: {e}")
        raise HTTPException(status_code=STATUS_BAD_REQUEST, detail=f"Login failed: {e}" )
    