from flask_restful import Resource
from src.shared.constants import (FOLDERS_DOWNLOAD_NAMES, STATUS_OK, STATUS_BAD_REQUEST)
from src.api.predictor.predictor import Predictor
import logging
from shapely.geometry import shape
from flask import request

logger = logging.getLogger(__name__)


class PredictorRequest(Resource):
    def post(self):
        try:
            data = request.get_json()
            end_date = data["end_date"]
            location = data["location"]
            initial_date = data["initial_date"]
            polygon = shape(location).wkt
            logger.info("----- Request post IntegrationsApi -----")
            logger.info(f"initial_date : {initial_date} - end_date : {end_date}")
            predictor = Predictor(polygon, location.get("coordinates"), initial_date, end_date)

            status, message = predictor.clean_folders()
            if status != STATUS_OK:
                return message, status

            status, message = predictor.get_polygon_images()

            if status != STATUS_OK:
                return message, status

            status, message = predictor.calculate_features()
            if status != STATUS_OK:
                return message, status

            status, message = predictor.feature_mean()
            if status != STATUS_OK:
                return message, status

            status, message = predictor.create_polygons()
            if status != STATUS_OK:
                return message, status

            status, message = predictor.create_dataset()
            if status != STATUS_OK:
                return message, status

            status, message = predictor.predict()
            if status != STATUS_OK:
                return message, status

            status, message = predictor.show_map()
            return message, status

        except Exception as e:
            logger.error(f"Error in post PredictorRequest: {e}")
            return {"message": f"images download failed : {e}"}, STATUS_BAD_REQUEST
