from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from shapely.geometry import shape
import logging
from src.shared.constants import STATUS_OK, STATUS_BAD_REQUEST
from src.api.predictor.predictor import Predictor
from src.request.predictor.schema import PredictorRequestBody
from src.request.predictor.docs import (
    summary_microplastic,
    description_microplastic,
    response_description_microplastic,
)

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post(
    "/microplastic",
    summary=summary_microplastic,
    description=description_microplastic,
    response_description=response_description_microplastic
)
async def predictor_request(data: PredictorRequestBody):
    try:
        polygon_wkt = shape(data.location.dict()).wkt
        logger.info(f"initial_date : {data.initial_date} - end_date : {data.end_date}")

        predictor = Predictor(polygon_wkt, data.location.coordinates, data.initial_date, data.end_date)

        for step in [
            predictor.clean_folders,
            predictor.get_polygon_images,
            predictor.calculate_features,
            predictor.feature_mean,
            predictor.create_polygons,
            predictor.create_dataset,
            predictor.predict,
            predictor.show_map,
        ]:
            status, message = step()
            if status != STATUS_OK:
                raise HTTPException(status_code=status, detail=message)
        logger.info("Predictor completed successfully.")
        return JSONResponse(status_code=200, content=message)

    except Exception as e:
        logger.error(f"Error in post PredictorRequest: {e}")
        raise HTTPException(status_code=STATUS_BAD_REQUEST, detail=f"images download failed: {e}")
