from flask_restful import Resource
from src.shared.constants import (FOLDERS_DOWNLOAD_NAMES, STATUS_BAD_REQUEST)
from src.api.predictor.predictor import Predictor
import logging
from shapely.geometry import shape
from flask import request

logger = logging.getLogger(__name__)


class PredictorRequest(Resource):
    def post(self):
        try:
            data = request.get_json()
            initial_date = data["initial_date"]
            end_date = data["end_date"]
            location = data["location"]
            coordinates = location["coordinates"]
            polygon = shape(location).wkt
            logger.info("----- Request post IntegrationsApi -----")
            logger.info(f"initial_date : {initial_date} - end_date : {end_date}")
            predictor = Predictor(FOLDERS_DOWNLOAD_NAMES)
            status, message = predictor.get_polygon_images(
                polygon, coordinates, initial_date, end_date)
            return message, status

        except Exception as e:
            logger.error(f"Error in post PredictorRequest: {e}")
            return {"message": f"images download failed : {e}"}, STATUS_BAD_REQUEST
