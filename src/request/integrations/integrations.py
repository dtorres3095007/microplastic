from flask_restful import Resource
from src.shared.constants import (FOLDERS_DOWNLOAD_NAMES, STATUS_BAD_REQUEST, STATUS_OK)
from src.api.integrations.integrations import Integrations
import logging
from shapely.geometry import shape
from flask import request

logger = logging.getLogger(__name__)


class IntegrationsRequest(Resource):
    def post(self):
        try:
            data = request.get_json()
            initial_date = data["initial_date"]
            end_date = data["end_date"]
            location = data["location"]
            polygon = shape(location).wkt
            logger.info("----- Request post IntegrationsApi -----")
            logger.info(f"initial_date : {initial_date} - end_date : {end_date}")
            integrations = Integrations(FOLDERS_DOWNLOAD_NAMES)
            status, message = integrations.get_images(polygon, initial_date, end_date)

            if status != STATUS_OK:
                logger.error(f"Error in get_images: {message}")
                return message, status

            status, message = integrations.clean_images()

            if status != STATUS_OK:
                logger.error(f"Error in clean_images: {message}")

            return {"message": "Images downloaded and cleaned successfully"}, STATUS_OK

        except Exception as e:
            logger.error(f"Error in post IntegrationsApi: {e}")
            return {"message": f"images download failed : {e}"}, STATUS_BAD_REQUEST
