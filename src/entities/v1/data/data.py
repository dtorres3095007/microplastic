
import copy
from shapely.geometry import shape
import logging
import json
from src.entities.v1.data.features.features import Feature
from src.shared.constants import DATES_MODEL_LIST, FEATURES_LIST, FOLDERS_MODEL_NAMES, MICROPLASTIC_DATA, POLYGONS_MODEL_LIST, STATUS_BAD_REQUEST, STATUS_OK
from src.entities.v1.integrations.integrations import Integrations
import os
from datetime import datetime, timedelta
import rasterio
from rasterio.transform import rowcol
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
                sub_folder = polygon_name
                folder_model["MAIN"] = folder_main + [sub_folder]

                integrations = Integrations(folder_model)
                status, message =  integrations.get_images(polygon, initial_date, end_date)
                if status != STATUS_OK:
                    logger.error(f"Error in getting images for polygon {polygon} and dates {initial_date} - {end_date}: {message}") 
        logger.info("----------------- Images downloaded -----------------")       
        return STATUS_OK, {"message": "Images downloaded."}
    
    def clean_model_images(self) -> tuple:
        """
        Clean images for the model polygons.
        """
        logger.info("----------------- Cleaning images for model polygons -----------------")
        for polygon_name in POLYGONS_MODEL_LIST:
            logger.info(f"Cleaning images for polygon {polygon_name}")
            folder_model = copy.deepcopy(FOLDERS_MODEL_NAMES)
            folder_main = folder_model.get("MAIN")
            sub_folder = polygon_name
            folder_model["MAIN"] = folder_main + [sub_folder]

            integrations = Integrations(folder_model)
            status, message =  integrations.clean_images()
            if status != STATUS_OK:
                logger.error(f"Error in cleaning images for polygon {polygon_name}: {message}") 
        logger.info("----------------- Images cleaned -----------------")       
        return STATUS_OK, {"message": "Images cleaned."}
    
    def calculate_features(self) -> tuple:
        """
        Calculate features for the model polygons.
        """
        try:
            logger.info("----------------- Calculating features for model polygons -----------------")
            base_dir = os.path.join(os.getcwd(), *FOLDERS_MODEL_NAMES["MAIN"])
            for polygon_folder in os.listdir(base_dir):
                polygon_path = os.path.join(base_dir, polygon_folder)
                cleaned_path = os.path.join(polygon_path, FOLDERS_MODEL_NAMES["CLEANED"])
                
                if not os.path.isdir(cleaned_path):
                    continue  # Skip if "cleaned" folder does not exist

                logger.info(f"Processing polygon: {polygon_folder}")
                for band_folder in os.listdir(cleaned_path):
                    band_path = os.path.join(cleaned_path, band_folder)
                    if not os.path.isdir(band_path):
                        continue
                    
                    band_files = {os.path.splitext(f)[0]: os.path.join(band_path, f) for f in os.listdir(band_path) if f.endswith(".tif")}
                    if band_files:
                        output_folder = os.path.join(polygon_path, FOLDERS_MODEL_NAMES["FEATURES"], band_folder)
                        os.makedirs(output_folder, exist_ok=True)
                        logger.info("Calculating features")
                        feature = Feature(band_files, output_folder)
                        logger.info("Opening bands")
                        feature.open_bands()
                        logger.info("Band opened")
                        status, message = feature.calculate_ndvi()
                        logger.info(f"calculate_ndvi Status: {status}, Message: {message}")
                        status, message = feature.calculate_ndwi()
                        logger.info(f"calculate_ndwi Status: {status}, Message: {message}")
                        status, message = feature.calculate_ndci()
                        logger.info(f"calculate_ndci Status: {status}, Message: {message}")
                        status, message = feature.calculate_fdi()
                        logger.info(f"calculate_fdi Status: {status}, Message: {message}")
                        status, message = feature.calculate_ndpi()
                        logger.info(f"calculate_ndpi Status: {status}, Message: {message}")
            logger.info("----------------- Features calculated -----------------")       
            return STATUS_OK, {"message": "Features calculated."}
        except Exception as e:
            logger.error(f"Error in calculate_features: {str(e)}")
            logger.info("----------------- Features calculated Error-----------------") 
            return STATUS_BAD_REQUEST, {"message": str(e)}

    def create_dataset(self) -> tuple:
        """
        create dataset for the model polygons.
        """
        try:
                                    
            logger.info("----------------- Create dataset for model polygons -----------------")
            base_dir = os.path.join(os.getcwd(), *FOLDERS_MODEL_NAMES["MAIN"])
            dataset = copy.deepcopy(MICROPLASTIC_DATA)
            for data in dataset:
                date = data.get("date")
                dataset_date = datetime.strptime(date, "%Y-%m-%d")
                folder = data.get("folder")
                latitude = data.get("latitude")
                longitude = data.get("longitude")
                polygon_path = os.path.join(base_dir, folder)
                fetures_path = os.path.join(polygon_path, FOLDERS_MODEL_NAMES["FEATURES"])
                logger.info(f"Processing polygon: {folder} - {date}")

                if not os.path.isdir(fetures_path):
                    logger.error(f"Processing polygon: {folder} - {date} - Error: fetures_path does not exist")
                    continue 

                for band_indicator_folder in os.listdir(fetures_path):
                    date_str = band_indicator_folder.split("_")[2][:8]
                    band_date = datetime.strptime(date_str, "%Y%m%d")
                    lower_bound = dataset_date - timedelta(days=3)
                    upper_bound = dataset_date + timedelta(days=3)

                    # Verificar si la fecha está dentro del rango de ±3 días
                    if lower_bound <= band_date <= upper_bound:
                        logger.info(f"Band {band_indicator_folder} is within range for {folder} - {date}")

                        band_path = os.path.join(fetures_path, band_indicator_folder)
                        for indicator_name in FEATURES_LIST:
                            indicator_file = os.path.join(band_path, f"{indicator_name}.tif")
                            if not os.path.isfile(indicator_file):
                                data[indicator_name] = None
                                logger.error(f"Indicator file {indicator_file} does not exist")
                                continue

                            with rasterio.open(indicator_file) as datasetIndicator:
                                # Convertir latitud y longitud a coordenadas de píxel
                                row, col = map(int, rowcol(datasetIndicator.transform, longitude, latitude))

                                # Leer el valor del píxel en esa ubicación
                                raw_value = datasetIndicator.read(1)[row, col]
                                value = (raw_value / 32767.5) - 1
                                # Guardar el valor en el datasetIndicator
                                data[indicator_name] = value
                                logger.info(f"Extracted {indicator_name}: {value} for {folder} and {date} and {band_indicator_folder}")
            return STATUS_OK, {"message": "Create Dataset."}
        except Exception as e:
            logger.error(f"Error in create_dataset: {str(e)}")
            logger.info("----------------- Create dataset Error-----------------") 
            return STATUS_BAD_REQUEST, {"message": str(e)}