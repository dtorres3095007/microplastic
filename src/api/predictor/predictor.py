from src.shared.constants import (
    FOLDERS_DOWNLOAD_NAMES,
    STATUS_BAD_REQUEST,
    FEATURES_LIST,
    FILE_GRID,
    FILE_DATASET_PREDICTOR,
    STATUS_OK)
import logging
from src.api.integrations.integrations import Integrations
import os
from src.entities.features.features import Feature
import rasterio
import numpy as np
import geopandas as gpd
from rasterio.mask import mask
import pandas as pd
import json
from shapely.geometry import shape
from rasterio.warp import transform_geom

logger = logging.getLogger(__name__)


class Predictor:
    def __init__(self, polygon, coordinates, initial_date, end_date):
        """
        Initialize the Predictor class.
        """
        self.integrations = Integrations(FOLDERS_DOWNLOAD_NAMES)
        self.polygon = polygon
        self.initial_date = initial_date
        self.end_date = end_date
        self.coordinates = coordinates[0]

    def get_polygon_images(self):
        """
        Get the images from the polygon.
        """
        status, message = self.integrations.get_images(
            self.polygon, self.initial_date, self.end_date)

        if status != STATUS_OK:
            logger.error(f"Error in get_images: {message}")
            return message, status

        status, message = self.integrations.clean_images()
        return message, status

    def calculate_features(self) -> tuple:
        """
        Calculate features for the model polygons.
        """
        try:
            logger.info("Calculating features")
            base_dir = os.path.join(
                os.getcwd(),
                *FOLDERS_DOWNLOAD_NAMES["MAIN"],
                FOLDERS_DOWNLOAD_NAMES["CLEANED"])
            for image_folder in os.listdir(base_dir):
                image_path = os.path.join(base_dir, image_folder)

                band_files = {
                    os.path.splitext(f)[0]: os.path.join(image_path, f)
                    for f in os.listdir(image_path)
                    if f.endswith(".tif")
                }
                if band_files:
                    output_folder = os.path.join(
                        *FOLDERS_DOWNLOAD_NAMES["MAIN"], FOLDERS_DOWNLOAD_NAMES["FEATURES"], image_folder
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

    def feature_mean(self):
        """
        Calculate the mean of the features.
        """
        try:

            for ind in FEATURES_LIST:
                sum_features = 0
                count = 0
                base_dir = os.path.join(
                    os.getcwd(),
                    *FOLDERS_DOWNLOAD_NAMES["MAIN"],
                    FOLDERS_DOWNLOAD_NAMES["FEATURES"])
                output_dir = os.path.join(
                    os.getcwd(),
                    *FOLDERS_DOWNLOAD_NAMES["MAIN"],
                    FOLDERS_DOWNLOAD_NAMES["FEATURES_MEAN"])
                os.makedirs(output_dir, exist_ok=True)

                for image_folder in os.listdir(base_dir):
                    image_path = os.path.join(base_dir, image_folder)
                    raster_path = os.path.join(image_path, f"{ind}.tif")

                    if os.path.exists(raster_path):
                        with rasterio.open(raster_path) as src:
                            image = src.read(1).astype(np.uint16)
                            image[image == src.nodata] = 0

                            if sum_features is None:
                                sum_features = np.zeros_like(image, dtype=np.uint32)

                            sum_features += image
                            count += 1

                if count > 0:
                    mean_feature = (
                        sum_features /
                        count).astype(
                        np.uint16)

                    output_path = os.path.join(output_dir, f"{ind}.tif")

                    with rasterio.open(raster_path) as src:
                        profile = src.profile.copy()

                    profile.update(
                        dtype=rasterio.uint16,
                        count=1,
                        nodata=0,
                        driver="GTiff"
                    )
                    with rasterio.open(output_path, "w", **profile) as dst:
                        dst.write(mean_feature, 1)
                        dst.crs = profile["crs"]

                    logger.info(f"Feature {ind} average calculated")
            return STATUS_OK, {"message": "Features average calculated."}
        except Exception as e:
            logger.error(f"Error in feature_average: {str(e)}")
            return STATUS_BAD_REQUEST, {"message": str(e)}

    def create_polygons(self):
        """
        Create the polygons for the model.
        """
        try:
            logger.info("Creating polygons")
            status, message = self.integrations.create_polygons_10m(self.coordinates)
            if status != STATUS_OK:
                logger.error(f"Error in create_polygons: {message}")
                return status, message
            logger.info("Polygons created")
            return STATUS_OK, {"message": "Polygons created."}
        except Exception as e:
            logger.error(f"Error in create_polygons: {str(e)}")
            return STATUS_BAD_REQUEST, {"message": str(e)}

    def create_dataset(self):
        """
        Create the dataset for the model.
        """
        try:
            logger.info("Creating dataset")
            # Load the 10m x 10m grid as a GeoDataFrame
            geojson = os.path.join(
                os.getcwd(),
                *FOLDERS_DOWNLOAD_NAMES["MAIN"],
                FOLDERS_DOWNLOAD_NAMES["POLYGONS"], FILE_GRID)

            with open(geojson, "r", encoding="utf-8") as file:
                geojson_data = json.load(file)

            polygons = []

            for feature in geojson_data["features"]:
                # Convert GeoJSON geometry to a Shapely Polygon
                polygon = shape(feature["geometry"])
                polygons.append(polygon)

            logger.info(f"Loaded {len(polygons)} polygons from GeoJSON.")

            # Dictionary to store extracted data
            data = {"polygon_id": [], "geometry": []}  # Store ID and geometry (WKT format)

            # Initialize feature columns in the dataset
            for ind in FEATURES_LIST:
                data[ind] = []

            # Iterate over each 10m x 10m polygon and extract feature values
            for idx, polygon in enumerate(polygons):
                polygon_id = idx + 1
                data["polygon_id"].append(polygon_id)
                data["geometry"].append(polygon.wkt)  # Store as WKT format for reference

                # Extract values from each feature (TIFF file)
                for ind in FEATURES_LIST:
                    raster_path = os.path.join(
                        os.getcwd(),
                        *FOLDERS_DOWNLOAD_NAMES["MAIN"],
                        FOLDERS_DOWNLOAD_NAMES["FEATURES_MEAN"], f"{ind}.tif")
                    if os.path.exists(raster_path):
                        with rasterio.open(raster_path) as src:
                            try:
                                print("crs", src.crs)
                                # Clip the raster to the cell's polygon area
                                # Transform polygon to match the raster's CRS
                                polygon_transformed = transform_geom(
                                    "EPSG:4326",  # Input CRS (lat/lon)
                                    src.crs,  # Target CRS (from raster)
                                    polygon.__geo_interface__,  # Convert Shapely to GeoJSON format
                                    precision=6  # Adjust precision for better accuracy
                                )

                                # Use the transformed polygon in mask()
                                out_image, _ = mask(src, [polygon_transformed], crop=True)
                                # Remove NoData values and compute the mean
                                valid_pixels = out_image[out_image != src.nodata]
                                # Convert values using the scaling formula if there are valid pixels
                                if valid_pixels.size > 0:
                                    mean_value = np.nanmean(valid_pixels)
                                    scaled_value = (
                                        mean_value / 32767.5) - 1  # Apply scaling formula
                                else:
                                    scaled_value = np.nan

                            except Exception as e:
                                logger.error(f"Error processing {ind} for cell {polygon_id}: {e}")
                                scaled_value = np.nan
                    else:
                        logger.info(f"⚠️ {ind}_mean.tif not found!")
                        scaled_value = np.nan

                    # Store the computed mean value for the feature
                    data[ind].append(scaled_value)

            # Convert the extracted data to a Pandas DataFrame
            df = pd.DataFrame(data)
            output_csv = os.path.join(
                os.getcwd(),
                *FOLDERS_DOWNLOAD_NAMES["MAIN"],
                FOLDERS_DOWNLOAD_NAMES["DATASET"])
            os.makedirs(output_csv, exist_ok=True)
            # Save the dataset as a CSV file
            df.to_csv(f"{output_csv}/{FILE_DATASET_PREDICTOR}", index=False)

            logger.info(f"Dataset successfully saved at: {output_csv}")
            return STATUS_OK, {"message": "Dataset created."}
        except Exception as e:
            logger.error(f"Error in create_dataset: {str(e)}")
            return STATUS_BAD_REQUEST, {"message": str(e)}
