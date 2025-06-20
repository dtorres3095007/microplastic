from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from fastapi import Query
import logging
from src.shared.constants import STATUS_OK, STATUS_BAD_REQUEST
from src.api.users.users_get_all.docs import (
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

async def users_get(
    limit: int = Query(10, gt=0, description="Maximum number of users to return"), 
    offset: int = Query(0, ge=0, description="Number of users to skip before starting to collect the result set"),
    search: str = Query(None, description="Search term to filter users by email")
    ):
    try:
        logger.info("Received users_get request")
        conn = DatabaseConnection()
        user = Users(conn)

        status, message = user.get_users(limit=limit, offset=offset, search=search)

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
    