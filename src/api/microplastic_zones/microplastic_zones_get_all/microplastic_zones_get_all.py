from fastapi import APIRouter, Request, Security, HTTPException, Depends
import logging
import os
from fastapi.security import APIKeyHeader
from src.api.microplastic_zones.microplastic_zones_get_all.docs import (
    summary_microplastic_zones_get_all,
    description_microplastic_zones_get_all,
    response_description_microplastic_zones_get_all,
)
from src.shared.decorators.api_key_guard import require_api_key
from src.shared.db_config import DatabaseConnection
from src.entities.microplastic_zones.microplastic_zones import MicroplasticZone
from src.shared.constants import STATUS_OK, STATUS_BAD_REQUEST
from fastapi.responses import JSONResponse
from src.api.microplastic_zones.microplastic_zones_get_all.schema import (
    MicroplasticZonesQueryParams,
)


router = APIRouter()
logger = logging.getLogger(__name__)

API_KEY_NAME = os.getenv("API_KEY_NAME")
api_key_header = APIKeyHeader(name=API_KEY_NAME)


@router.get(
    "/microplastic_zones",
    summary=summary_microplastic_zones_get_all,
    description=description_microplastic_zones_get_all,
    response_description=response_description_microplastic_zones_get_all,
)
@require_api_key
async def get_all_microplastic_zones(
    request: Request,
    query: MicroplasticZonesQueryParams = Depends(),
    _: str = Security(api_key_header),
):
    try:
        logger.info("Received get_all_microplastic_zones request")
        conn = DatabaseConnection()
        microplastic_zone = MicroplasticZone(conn)

        status, message = await microplastic_zone.get_all_microplastic_zones(
            limit=query.limit,
            offset=query.offset,
            pred_min=query.pred_min,
            pred_max=query.pred_max,
            month=query.month,
            year=query.year,
        )

        if status == STATUS_OK:
            logger.info("Microplastic zones retrieved successfully.")
            return JSONResponse(status_code=STATUS_OK, content=message)

    except Exception as e:
        logger.error(f"Error in get_all_microplastic_zones: {e}")
        raise HTTPException(
            status_code=STATUS_BAD_REQUEST,
            detail=f"Failed to retrieve microplastic zones: {e}",
        )
