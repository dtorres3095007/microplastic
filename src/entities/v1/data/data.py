
import copy
from shapely.geometry import shape
import logging
import json
from src.shared.constants import DATES_MODEL_LIST, FOLDERS_MODEL_NAMES, POLYGONS_MODEL_LIST, STATUS_OK
from src.entities.v1.integrations.integrations import Integrations

logger = logging.getLogger(__name__)


class Data:
    def __init__(self):
        """
        Initialize the Data class.
        """

    def get_model_images(self) -> dict:
        """
        Get images for the model polygons and dates.
        """
        logger.info("----------------- Getting images for model polygons -----------------")
        for polygon_name in POLYGONS_MODEL_LIST:
            logger.info(f"Getting images for polygon {polygon_name}")
            with open(f"src/shared/model_polygons/{polygon_name}") as f:
                    geojson_data = json.load(f)
            geom = geojson_data["features"][0]["geometry"]
            polygon = shape(geom).wkt
            for dates in DATES_MODEL_LIST:
                initial_date = dates.get("initial_date")
                end_date = dates.get("end_date")
                logger.info(f"Getting images for dates {initial_date} - {end_date}")
                folder_model = copy.deepcopy(FOLDERS_MODEL_NAMES)
                folder_main = folder_model.get("MAIN")
                sub_folder = polygon_name.split(".json")[0]
                folder_model["MAIN"] = folder_main + [sub_folder]

                integrations = Integrations(folder_model)
                status, message =  integrations.get_images(polygon, initial_date, end_date)
                if status != STATUS_OK:
                    logger.error(f"Error in getting images for polygon {polygon} and dates {initial_date} - {end_date}: {message}") 
        logger.info("----------------- Images downloaded -----------------")       
        return STATUS_OK, {"message": "Images downloaded."}
    
    def clean_model_images(self) -> dict:
        """
        Clean images for the model polygons.
        """
        logger.info("----------------- Cleaning images for model polygons -----------------")
        for polygon_name in POLYGONS_MODEL_LIST:
            logger.info(f"Cleaning images for polygon {polygon_name}")
            folder_model = copy.deepcopy(FOLDERS_MODEL_NAMES)
            folder_main = folder_model.get("MAIN")
            sub_folder = polygon_name.split(".json")[0]
            folder_model["MAIN"] = folder_main + [sub_folder]

            integrations = Integrations(folder_model)
            status, message =  integrations.clean_images()
            if status != STATUS_OK:
                logger.error(f"Error in cleaning images for polygon {polygon_name}: {message}") 
        logger.info("----------------- Images cleaned -----------------")       
        return STATUS_OK, {"message": "Images cleaned."}