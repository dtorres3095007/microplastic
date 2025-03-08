from flask_restful import Resource
from src.entities.v1.integrations.integrations import Integrations
import logging
import json
from shapely.geometry import shape
from flask import request

logger = logging.getLogger(__name__)

class IntegrationsApi(Resource):
    def post(self):
        try:
            with open("local_test/map.geojson") as f:
                geojson_data = json.load(f)

            geom = geojson_data["features"][0]["geometry"]
            polygon = shape(geom).wkt

            data = request.get_json()
            initial_date = data["initial_date"]
            end_date = data["end_date"]
            logger.info(f"----- Request post IntegrationsApi -----")
            logger.info(f"data : {data}")
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
            return {"message": "images download failed"}, 400
