from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
import logging
from src.shared.constants import STATUS_OK, STATUS_BAD_REQUEST
from src.api.users.users_patch.docs import (
    summary_users_patch,
    description_users_patch,
    response_description_users_patch,
)
from src.api.users.users_patch.schema import UserPatchRequestBody
from src.shared.db_config import DatabaseConnection
from src.entities.users.users import Users


router = APIRouter()
logger = logging.getLogger(__name__)


@router.patch(
    "/{user_id}",
    summary=summary_users_patch,
    description=description_users_patch,
    response_description=response_description_users_patch,
)
async def users_patch(user_id: int, data: UserPatchRequestBody):
    try:
        logger.info(f"Received users_patch request: {data} for user_id: {user_id}")
        conn = DatabaseConnection()
        user = Users(conn)

        status, message = user.patch_user(
            user_id=user_id, email=data.email, profile=data.profile, active=data.active
        )

        if status != STATUS_OK:
            return JSONResponse(
                status_code=status, content={"message": message["message"]}
            )

        return JSONResponse(status_code=STATUS_OK, content=message)

    except Exception as e:
        logger.error(f"Error in users_patch: {e}")
        raise HTTPException(status_code=STATUS_BAD_REQUEST, detail=f"Patch failed: {e}")
