from fastapi import APIRouter, HTTPException, Request, Security, Depends
from fastapi.responses import JSONResponse
import logging
from src.shared.constants import STATUS_OK, STATUS_BAD_REQUEST
from src.entities.microplastic_zones.microplastic_zones import MicroplasticZone
from src.api.microplastic_zones.microplastic_zones_post.docs import (
    summary_microplastic_zones_post,
    description_microplastic_zones_post,
    response_description_microplastic_zones_post,
)
from src.shared.db_config import DatabaseConnection
from src.api.microplastic_zones.microplastic_zones_post.schema import (
    MicroplasticZoneForm,
)
from src.shared.decorators.api_key_guard import require_api_key
from fastapi.security import APIKeyHeader
import os

router = APIRouter()
logger = logging.getLogger(__name__)

API_KEY_NAME = os.getenv("API_KEY_NAME")
api_key_header = APIKeyHeader(name=API_KEY_NAME)


@router.post(
    "/microplastic_zones",
    summary=summary_microplastic_zones_post,
    description=description_microplastic_zones_post,
    response_description=response_description_microplastic_zones_post,
)
@require_api_key
async def create_microplastic_zone(
    request: Request,
    form: MicroplasticZoneForm = Depends(MicroplasticZoneForm.as_form),
    _: str = Security(api_key_header),
):
    try:
        logger.info(f"Received create_microplastic_zone request with data: {form}")
        conn = DatabaseConnection()
        microplastic_zone = MicroplasticZone(conn)

        status, message = await microplastic_zone.insert_microplastic_zone(form.file)

        if status != STATUS_OK:
            raise HTTPException(status_code=status, detail=message)

        logger.info("Microplastic zone created successfully.")
        return JSONResponse(status_code=200, content=message)

    except Exception as e:
        logger.error(f"Error in create_microplastic_zone: {e}")
        raise HTTPException(
            status_code=STATUS_BAD_REQUEST,
            detail=f"Microplastic zone creation failed: {e}",
        )
