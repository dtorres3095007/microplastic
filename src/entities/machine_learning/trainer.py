from pyproj import CRS
import copy
from shapely.geometry import shape
import logging
import json
from src.entities.machine_learning.src.models.models import Models
from src.shared.utils import save_dataset_to_csv
from src.entities.machine_learning.src.features.features import Feature
from src.shared.constants import (
    DATES_MODEL_LIST,
    FEATURE_FDI,
    FEATURE_NDCI,
    FEATURE_NDPI,
    FEATURE_NDVI,
    FEATURE_NDWI,
    FEATURES_LIST,
    FOLDER_POLYGONS,
    FOLDERS_DATASET_NAMES,
    FOLDERS_MODEL_NAMES,
    MICROPLASTIC_DATA,
    POLYGONS_MODEL_LIST,
    STATUS_BAD_REQUEST,
    STATUS_OK,
)
from src.entities.machine_learning.src.integrations import Integrations
import os
from datetime import datetime, timedelta
import rasterio
from rasterio.transform import rowcol
from rasterio.warp import transform

logger = logging.getLogger(__name__)


class Trainer:
    def __init__(self):
        """
        Initialize the Trainer class.
        """

    def get_model_images(self) -> dict:
        """
        Get images for the model polygons and dates.
        """
        logger.info("Getting images")
        for polygon_name in POLYGONS_MODEL_LIST:
            logger.info(f"Getting images for polygon {polygon_name}")
            base_dir = os.path.join(
                os.getcwd(), *FOLDER_POLYGONS, f"{polygon_name}.json"
            )

            with open(base_dir) as f:
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
                status, message = integrations.get_images(
                    polygon, initial_date, end_date
                )
                if status != STATUS_OK:
                    logger.error(
                        f"Error in getting images for polygon {polygon} and dates {initial_date} - {end_date}: {message}"
                    )
        logger.info("Images downloaded")
        return STATUS_OK, {"message": "Images downloaded."}

    def clean_model_images(self) -> tuple:
        """
        Clean images for the model polygons.
        """
        logger.info("Cleaning images")
        for polygon_name in POLYGONS_MODEL_LIST:
            logger.info(f"Cleaning images for polygon {polygon_name}")
            folder_model = copy.deepcopy(FOLDERS_MODEL_NAMES)
            folder_main = folder_model.get("MAIN")
            sub_folder = polygon_name
            folder_model["MAIN"] = folder_main + [sub_folder]

            integrations = Integrations(folder_model)
            status, message = integrations.clean_images()
            if status != STATUS_OK:
                logger.error(
                    f"Error in cleaning images for polygon {polygon_name}: {message}"
                )
        logger.info("Images cleaned")
        return STATUS_OK, {"message": "Images cleaned."}

    def calculate_features(self) -> tuple:
        """
        Calculate features for the model polygons.
        """
        try:
            logger.info("Calculating features")
            base_dir = os.path.join(os.getcwd(), *FOLDERS_MODEL_NAMES["MAIN"])
            for polygon_folder in os.listdir(base_dir):
                polygon_path = os.path.join(base_dir, polygon_folder)
                cleaned_path = os.path.join(
                    polygon_path, FOLDERS_MODEL_NAMES["CLEANED"]
                )

                if not os.path.isdir(cleaned_path):
                    continue  # Skip if "cleaned" folder does not exist

                logger.info(f"Processing polygon: {polygon_folder}")
                for band_folder in os.listdir(cleaned_path):
                    band_path = os.path.join(cleaned_path, band_folder)
                    if not os.path.isdir(band_path):
                        continue

                    band_files = {
                        os.path.splitext(f)[0]: os.path.join(band_path, f)
                        for f in os.listdir(band_path)
                        if f.endswith(".tif")
                    }
                    if band_files:
                        output_folder = os.path.join(
                            polygon_path, FOLDERS_MODEL_NAMES["FEATURES"], band_folder
                        )
                        os.makedirs(output_folder, exist_ok=True)
                        logger.info("Calculating features")
                        feature = Feature(band_files, output_folder)
                        status, message = feature.open_bands()
                        if status != STATUS_OK:
                            logger.error(f"Error in open_bands: {message}")
                            return status, message

                        status, message = feature.calculate_ndvi()
                        if status != STATUS_OK:
                            logger.error(f"Error in calculate_ndvi: {message}")
                        status, message = feature.calculate_ndwi()
                        if status != STATUS_OK:
                            logger.error(f"Error in calculate_ndwi: {message}")
                        status, message = feature.calculate_ndci()
                        if status != STATUS_OK:
                            logger.error(f"Error in calculate_ndci: {message}")
                        status, message = feature.calculate_fdi()
                        if status != STATUS_OK:
                            logger.error(f"Error in calculate_fdi: {message}")
                        status, message = feature.calculate_ndpi()
                        if status != STATUS_OK:
                            logger.error(f"Error in calculate_ndpi: {message}")
            logger.info("Features calculated")
            return STATUS_OK, {"message": "Features calculated."}
        except Exception as e:
            logger.error(f"Error in calculate_features: {str(e)}")
            return STATUS_BAD_REQUEST, {"message": str(e)}

    def create_dataset(self) -> tuple:
        """
        create dataset for the model polygons.
        """
        try:
            logger.info("Creating dataset")
            base_dir = os.path.join(os.getcwd(), *FOLDERS_MODEL_NAMES["MAIN"])
            dataset = copy.deepcopy(MICROPLASTIC_DATA)
            for data in dataset:
                date = data.get("date")
                dataset_date = datetime.strptime(date, "%Y-%m-%d")
                folder = data.get("folder")
                latitude = data.get("latitude")
                longitude = data.get("longitude")
                polygon_path = os.path.join(base_dir, folder)
                features_path = os.path.join(
                    polygon_path, FOLDERS_MODEL_NAMES["FEATURES"]
                )
                logger.info(f"Processing polygon: {folder} - {date}")

                indicators = {
                    FEATURE_NDVI: [],
                    FEATURE_NDWI: [],
                    FEATURE_NDCI: [],
                    FEATURE_FDI: [],
                    FEATURE_NDPI: [],
                }

                if not os.path.isdir(features_path):
                    logger.error(
                        f"Processing polygon: {folder} - {date} - Error: features_path does not exist"
                    )
                    continue

                for band_indicator_folder in os.listdir(features_path):
                    date_str = band_indicator_folder.split("_")[2][:8]
                    band_date = datetime.strptime(date_str, "%Y%m%d")
                    lower_bound = dataset_date - timedelta(days=3)
                    upper_bound = dataset_date + timedelta(days=3)

                    if lower_bound <= band_date <= upper_bound:
                        logger.info(
                            f"Band {band_indicator_folder} is within range for {folder} - {date}"
                        )

                        band_path = os.path.join(features_path, band_indicator_folder)
                        for indicator_name in FEATURES_LIST:
                            indicator_file = os.path.join(
                                band_path, f"{indicator_name}.tif"
                            )
                            if not os.path.isfile(indicator_file):
                                data[indicator_name] = None
                                logger.error(
                                    f"Indicator file {indicator_file} does not exist"
                                )
                                continue

                            with rasterio.open(indicator_file) as datasetIndicator:
                                image_crs = datasetIndicator.crs
                                lon_utm, lat_utm = transform(
                                    CRS.from_epsg(4326),
                                    image_crs,
                                    [longitude],
                                    [latitude],
                                )
                                row, col = map(
                                    int,
                                    rowcol(
                                        datasetIndicator.transform,
                                        lon_utm[0],
                                        lat_utm[0],
                                    ),
                                )
                                raw_value = datasetIndicator.read(1)[row, col]
                                value = (raw_value / 32767.5) - 1
                                indicators[indicator_name].append(value)
                                logger.info(
                                    f"Extracted {indicator_name}: {value} for {folder} and {date} and {band_indicator_folder}"
                                )

                for indicator_name in FEATURES_LIST:
                    if indicators[indicator_name]:
                        data[indicator_name] = sum(indicators[indicator_name]) / len(
                            indicators[indicator_name]
                        )
                    else:
                        data[indicator_name] = None
            dataset_path = os.path.join(
                *FOLDERS_DATASET_NAMES["MAIN"], FOLDERS_DATASET_NAMES["DATASET"]
            )
            status, message = save_dataset_to_csv(dataset, dataset_path)
            if not status:
                logger.error(f"Error in save_dataset_to_csv: {message}")
                return STATUS_BAD_REQUEST, {"message": message}
            logger.info("Dataset created")
            return STATUS_OK, {"message": "Create Dataset."}
        except Exception as e:
            logger.error(f"Error in create_dataset: {str(e)}")
            return STATUS_BAD_REQUEST, {"message": str(e)}

    def train_models(self) -> tuple:
        """
        Train models for the dataset.
        """
        try:
            logger.info("Training models for the dataset")
            dataset_path = os.path.join(
                *FOLDERS_DATASET_NAMES["MAIN"],
                FOLDERS_DATASET_NAMES["DATASET"],
                "microplastics.csv",
            )
            models_path = os.path.join(
                *FOLDERS_DATASET_NAMES["MAIN"], FOLDERS_DATASET_NAMES["MODELS"]
            )
            # Initialize model class
            model_trainer = Models(dataset_path, models_path)

            # Load data
            status, response = model_trainer.load_data()
            if status != STATUS_OK:
                logger.error(f"Error in load_data: {response}")
                return status, response
            df = response

            # Split data
            status, response = model_trainer.split_data(df)
            if status != STATUS_OK:
                logger.error(f"Error in split_data: {response}")
                return status, response
            X_train, X_test, y_train, y_test = response

            # Train models
            status, response = model_trainer.train_models(X_train, y_train)
            if status != STATUS_OK:
                logger.error(f"Error in train_models: {response}")
                return status, response

            # Evaluate models
            status, response = model_trainer.evaluate_models(X_test, y_test)
            if status != STATUS_OK:
                logger.error(f"Error in evaluate_models: {response}")
                return status, response

            # Save models
            status, response = model_trainer.save_models()
            if status != STATUS_OK:
                logger.error(f"Error in save_models: {response}")
                return status, response
            logger.info("Models trained.")
            return STATUS_OK, {"message": "Models trained."}
        except Exception as e:
            logger.error(f"Error in train_models: {str(e)}")
            return STATUS_BAD_REQUEST, {"message": str(e)}

    def evaluate_models(self) -> tuple:
        """
        Evaluate models for the dataset.
        """
        try:
            logger.info("Evaluating models for the dataset")
            dataset_path = os.path.join(
                *FOLDERS_DATASET_NAMES["MAIN"],
                FOLDERS_DATASET_NAMES["DATASET"],
                "microplastics.csv",
            )
            models_path = os.path.join(
                *FOLDERS_DATASET_NAMES["MAIN"], FOLDERS_DATASET_NAMES["MODELS"]
            )
            # Initialize model class
            model_trainer = Models(dataset_path, models_path)

            status, response = model_trainer.load_data()
            if status != STATUS_OK:
                logger.error(f"Error in load_data: {response}")
                return status, response
            df = response

            status, response = model_trainer.load_models()
            if status != STATUS_OK:
                logger.error(f"Error in load_models: {response}")
                return status, response

            X = df[model_trainer.features]
            y = df[model_trainer.target]

            X_scaled = model_trainer.scaler.transform(X)
            status, response = model_trainer.evaluate_models(X_scaled, y)

            if status != STATUS_OK:
                logger.error(f"Error in evaluate_models: {response}")
                return status, response
            logger.info(f"Model evaluation: {response}")
            return STATUS_OK, response

        except Exception as e:
            logger.error(f"Error in evaluate_models: {str(e)}")
            return STATUS_BAD_REQUEST, {"message": str(e)}
