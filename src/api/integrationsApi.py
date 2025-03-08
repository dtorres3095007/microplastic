from flask_restful import Resource
from src.entities.v1.integrations.integrations import Integrations
import logging
import json
from shapely.geometry import shape
from flask import request
import base64

logger = logging.getLogger(__name__)

class IntegrationsApi(Resource):
    def post(self):
        try:
            data = request.get_json()
            initial_date = data["initial_date"]
            end_date = data["end_date"]
            location = data["location"]
            file_data = base64.b64decode(location).decode('utf-8')
            geojson_data = json.loads(file_data)
            geom = geojson_data["features"][0]["geometry"]
            polygon = shape(geom).wkt
            logger.info("----- Request post IntegrationsApi -----")
            logger.info(f"initial_date : {initial_date} - end_date : {end_date}")
            integrations = Integrations()
            status, message = integrations.get_images(polygon, initial_date, end_date)

            if status != 200:
                logger.error(f"Error in get_images: {message}")
                return message, status
            
            status, message = integrations.clean_images()

            if status != 200:
                logger.error(f"Error in clean_images: {message}")

            return {"message" : "Images downloaded and cleaned successfully"}, 200

        except Exception as e:
            logger.error(f"Error in post IntegrationsApi: {e}")
            return {"message": f"images download failed : {e}"}, 400
