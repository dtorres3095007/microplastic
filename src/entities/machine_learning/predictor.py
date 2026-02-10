from src.shared.constants import (
    FOLDERS_DOWNLOAD_NAMES,
    STATUS_BAD_REQUEST,
    FEATURES_LIST,
    FILE_GRID,
    FILE_DATASET_INDICATORS,
    FILE_DATASET_WITH_PREDICTIONS,
    FILE_MAP_PREDICTIONS,
    FOLDERS_DATASET_NAMES,
    BEST_MODEL,
    FEATURE_FDI,
    FEATURE_NDCI,
    FEATURE_NDPI,
    FEATURE_NDVI,
    FEATURE_NDWI,
    BANDS_LIST,
    BAND_BLUE,
    BAND_GREEN,
    BAND_RED,
    BAND_REDEDGE1,
    BAND_REDEDGE2,
    BAND_REDEDGE3,
    BAND_NIR_10M,
    BAND_NIR_20M,
    BAND_SWIR1,
    BAND_SWIR2,
    STATUS_OK,
)
import logging
from src.entities.machine_learning.src.integrations import Integrations
import os
from src.entities.machine_learning.src.features.features import Feature
import rasterio
import numpy as np
import geopandas as gpd
from rasterio.mask import mask
import pandas as pd
import json
from shapely.geometry import shape
from rasterio.warp import transform_geom
from src.entities.machine_learning.src.models.models import Models
import folium
from shapely.wkt import loads
import shutil
from src.entities.machine_learning.outputs_db import OutputsDB

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

    def clean_folders(self):
        """
        Clean the folders in data_predictor.
        """
        try:
            logger.info("Cleaning folders")
            folder_path = os.path.join(*FOLDERS_DOWNLOAD_NAMES["MAIN"])
            if os.path.exists(folder_path):
                shutil.rmtree(folder_path)
                logger.info("Folders cleaned")
            os.makedirs(folder_path, exist_ok=True)
            return STATUS_OK, {"message": "Folders cleaned."}
        except Exception as e:
            logger.error(f"Error in clean_folders: {str(e)}")
            return STATUS_BAD_REQUEST, {"message": str(e)}

    def get_polygon_images(self):
        """
        Get the images from the polygon.
        """
        status, message = self.integrations.get_images(
            self.polygon, self.initial_date, self.end_date
        )
        logger.info(f"Images downloaded : {message} - {status}")
        if status != STATUS_OK:
            logger.error(f"Error in get_images: {message}")
            return status, message
        status, message = self.integrations.clean_images()
        logger.info(f"Images cleaned : {message} - {status}")

        return status, message

    def calculate_features(self) -> tuple:
        """
        Calculate features for the model polygons.
        """
        try:
            logger.info("Calculating features")
            base_dir = os.path.join(
                os.getcwd(),
                *FOLDERS_DOWNLOAD_NAMES["MAIN"],
                FOLDERS_DOWNLOAD_NAMES["CLEANED"],
            )
            for image_folder in os.listdir(base_dir):
                image_path = os.path.join(base_dir, image_folder)

                band_files = {
                    os.path.splitext(f)[0]: os.path.join(image_path, f)
                    for f in os.listdir(image_path)
                    if f.endswith(".tif")
                }
                if band_files:
                    output_folder = os.path.join(
                        *FOLDERS_DOWNLOAD_NAMES["MAIN"],
                        FOLDERS_DOWNLOAD_NAMES["FEATURES"],
                        image_folder,
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
        Calculate the mean of the features stored as uint16 scaled [-1,1],
        and save the mean as float32 (real values).
        """
        try:
            base_dir = os.path.join(
                os.getcwd(),
                *FOLDERS_DOWNLOAD_NAMES["MAIN"],
                FOLDERS_DOWNLOAD_NAMES["FEATURES"],
            )
            output_dir = os.path.join(
                os.getcwd(),
                *FOLDERS_DOWNLOAD_NAMES["MAIN"],
                FOLDERS_DOWNLOAD_NAMES["FEATURES_MEAN"],
            )
            os.makedirs(output_dir, exist_ok=True)

            for ind in FEATURES_LIST:
                sum_features = None
                count_valid = None
                ref_profile = None

                # recorrer todas las imágenes
                for image_folder in os.listdir(base_dir):
                    raster_path = os.path.join(base_dir, image_folder, f"{ind}.tif")
                    if not os.path.exists(raster_path):
                        continue

                    with rasterio.open(raster_path) as src:
                        arr_u16 = src.read(1)
                        nodata = src.nodata or 0  # en tu caso usaste 0
                        if ref_profile is None:
                            ref_profile = src.profile.copy()

                        # máscara de valores válidos
                        valid_mask = arr_u16 != nodata

                        # desescalar a float32 [-1, 1]
                        arr_f32 = arr_u16.astype(np.float32) / 32767.5 - 1.0

                        # inicializar acumuladores
                        if sum_features is None:
                            sum_features = np.zeros_like(arr_f32, dtype=np.float32)
                            count_valid = np.zeros_like(arr_u16, dtype=np.uint16)

                        # acumular solo donde hay datos válidos
                        sum_features[valid_mask] += arr_f32[valid_mask]
                        count_valid[valid_mask] += 1

                # calcular promedio
                if ref_profile is not None:
                    mean_f32 = np.full_like(sum_features, np.nan, dtype=np.float32)
                    valid_any = count_valid > 0
                    mean_f32[valid_any] = (
                        sum_features[valid_any] / count_valid[valid_any]
                    )

                    # guardar en float32 con nodata=-9999
                    output_path = os.path.join(output_dir, f"{ind}.tif")
                    prof = ref_profile.copy()
                    prof.update(
                        dtype=rasterio.float32, nodata=-9999.0, count=1, driver="GTiff"
                    )

                    with rasterio.open(output_path, "w", **prof) as dst:
                        # sustituimos NaN por -9999
                        out_arr = np.where(
                            np.isnan(mean_f32), -9999.0, mean_f32
                        ).astype(np.float32)
                        dst.write(out_arr, 1)
                        dst.write_mask((valid_any.astype(np.uint8)) * 255)
                        dst.crs = prof["crs"]

                    logger.info(f"✅ Feature {ind} average calculated")

            return STATUS_OK, {"message": "Features mean saved in float32."}

        except Exception as e:
            logger.error(f"Error in feature_mean: {str(e)}")
            return STATUS_BAD_REQUEST, {"message": str(e)}

    def bands_means(self):
        try:
            for band in BANDS_LIST:
                sum_bands = 0
                count = 0
                base_dir = os.path.join(
                    os.getcwd(),
                    *FOLDERS_DOWNLOAD_NAMES["MAIN"],
                    FOLDERS_DOWNLOAD_NAMES["CLEANED"],
                )
                output_dir = os.path.join(
                    os.getcwd(),
                    *FOLDERS_DOWNLOAD_NAMES["MAIN"],
                    FOLDERS_DOWNLOAD_NAMES["BANDS_MEAN"],
                )
                os.makedirs(output_dir, exist_ok=True)

                for folder in os.listdir(base_dir):
                    folder_path = os.path.join(base_dir, folder)
                    band_file = os.path.join(folder_path, f"{band}.tif")

                    if os.path.exists(band_file):
                        with rasterio.open(band_file) as src:
                            image = src.read(1).astype(np.uint16)
                            image[image == src.nodata] = 0

                            if sum_bands is None:
                                sum_bands = np.zeros_like(image, dtype=np.uint32)

                            sum_bands += image
                            count += 1

                if count > 0:
                    mean_band = (sum_bands / count).astype(np.uint16)
                    output_path = os.path.join(output_dir, f"{band}.tif")

                    with rasterio.open(band_file) as src:
                        profile = src.profile.copy()

                    profile.update(
                        dtype=rasterio.uint16, count=1, nodata=0, driver="GTiff"
                    )
                    with rasterio.open(output_path, "w", **profile) as dst:
                        dst.write(mean_band, 1)
                        dst.crs = profile["crs"]

                    logger.info(f"Band {band} average calculated")
            return STATUS_OK, {"message": "Features average calculated."}
        except Exception as e:
            logger.error(f"Error in bands_means: {str(e)}")
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
                FOLDERS_DOWNLOAD_NAMES["POLYGONS"],
                FILE_GRID,
            )

            with open(geojson, "r", encoding="utf-8") as file:
                geojson_data = json.load(file)

            polygons = []

            for feature in geojson_data["features"]:
                # Convert GeoJSON geometry to a Shapely Polygon
                polygon = shape(feature["geometry"])
                polygons.append(polygon)

            logger.info(f"Loaded {len(polygons)} polygons from GeoJSON.")

            # Dictionary to store extracted data
            data = {
                "polygon_id": [],
                "geometry": [],
            }  # Store ID and geometry (WKT format)

            # Initialize feature columns in the dataset
            for ind in FEATURES_LIST + BANDS_LIST:
                data[ind] = []

            # Iterate over each 10m x 10m polygon and extract feature values
            for idx, polygon in enumerate(polygons):
                polygon_id = idx + 1
                data["polygon_id"].append(polygon_id)
                data["geometry"].append(
                    polygon.wkt
                )  # Store as WKT format for reference

                # Extract band values
                for band in BANDS_LIST:
                    band_folder = os.path.join(
                        os.getcwd(),
                        *FOLDERS_DOWNLOAD_NAMES["MAIN"],
                        FOLDERS_DOWNLOAD_NAMES["BANDS_MEAN"],
                    )
                    band_file = os.path.join(band_folder, f"{band}.tif")
                    if os.path.exists(band_file):
                        with rasterio.open(band_file) as src:
                            try:
                                print("crs band", src.crs)
                                # Clip the raster to the cell's polygon area
                                polygon_transformed = transform_geom(
                                    "EPSG:4326",  # Input CRS (lat/lon)
                                    src.crs,  # Target CRS (from raster)
                                    polygon.__geo_interface__,  # Convert Shapely to GeoJSON format
                                    precision=6,  # Adjust precision for better accuracy
                                )

                                out_image, _ = mask(
                                    src, [polygon_transformed], crop=True
                                )
                                # Remove NoData values and compute the mean
                                valid_pixels = out_image[out_image != src.nodata]
                                # Convert values using the scaling formula if there are valid pixels
                                if valid_pixels.size > 0:
                                    mean_value = np.nanmean(valid_pixels)
                                    scaled_value = mean_value / 10000.0
                                else:
                                    scaled_value = np.nan

                            except Exception as e:
                                logger.error(f"Error processing {band}: {e}")
                                scaled_value = np.nan
                    else:
                        logger.info(f"⚠️ {band}.tif not found!")
                        scaled_value = np.nan

                    data[band].append(scaled_value)

                # Extract values from each feature (TIFF file)
                for ind in FEATURES_LIST:
                    raster_path = os.path.join(
                        os.getcwd(),
                        *FOLDERS_DOWNLOAD_NAMES["MAIN"],
                        FOLDERS_DOWNLOAD_NAMES["FEATURES_MEAN"],
                        f"{ind}.tif",
                    )
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
                                    precision=6,  # Adjust precision for better accuracy
                                )

                                # Use the transformed polygon in mask()
                                out_image, _ = mask(
                                    src, [polygon_transformed], crop=True
                                )
                                # Remove NoData values and compute the mean
                                valid_pixels = out_image[out_image != src.nodata]
                                # Convert values using the scaling formula if there are valid pixels
                                if valid_pixels.size > 0:
                                    mean_value = np.nanmean(valid_pixels)
                                    scaled_value = mean_value
                                else:
                                    scaled_value = np.nan

                            except Exception as e:
                                logger.error(
                                    f"Error processing {ind} for cell {polygon_id}: {e}"
                                )
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
                FOLDERS_DOWNLOAD_NAMES["DATASET"],
            )
            os.makedirs(output_csv, exist_ok=True)
            # Save the dataset as a CSV file
            df.to_csv(f"{output_csv}/{FILE_DATASET_INDICATORS}", index=False)

            logger.info(f"Dataset successfully saved at: {output_csv}")
            return STATUS_OK, {"message": "Dataset created."}
        except Exception as e:
            logger.error(f"Error in create_dataset: {str(e)}")
            return STATUS_BAD_REQUEST, {"message": str(e)}

    def predict(self):
        """
        Predict the microplastic concentration.
        """
        dataset_path = os.path.join(
            *FOLDERS_DOWNLOAD_NAMES["MAIN"],
            FOLDERS_DOWNLOAD_NAMES["DATASET"],
            FILE_DATASET_INDICATORS,
        )
        models_path = os.path.join(
            *FOLDERS_DATASET_NAMES["MAIN"], FOLDERS_DATASET_NAMES["MODELS"]
        )
        model = Models(dataset_path, models_path)
        print("model.__dict__ =", model.__dict__)
        status, message = model.load_data()

        if status != STATUS_OK:
            return status, message

        df = message

        status, message = model.load_models()

        models = model.models
        scaler = model.scaler
        X = df[model.features]
        linear_model = models["Linear Regression"]
        random_forest = models["Random Forest"]
        neural_network = models["Neural Network"]
        X_scaled = scaler.transform(X)
        df["pred_linear"] = linear_model.predict(X_scaled)
        df["pred_forest"] = random_forest.predict(X_scaled)
        df["pred_neural"] = neural_network.predict(X_scaled)
        output_path = os.path.join(
            *FOLDERS_DOWNLOAD_NAMES["MAIN"],
            FOLDERS_DOWNLOAD_NAMES["DATASET"],
            FILE_DATASET_WITH_PREDICTIONS,
        )
        df.to_csv(output_path, index=False)
        return STATUS_OK, {"message": "Predictions saved successfully."}

    def show_map(self):
        """
        Show the map with the polygons.
        """
        try:
            # Load the dataset with predictions
            csv_file = os.path.join(
                *FOLDERS_DOWNLOAD_NAMES["MAIN"],
                FOLDERS_DOWNLOAD_NAMES["DATASET"],
                FILE_DATASET_WITH_PREDICTIONS,
            )
            df = pd.read_csv(csv_file)
            PRED_MIN, PRED_MAX = 0.0, 2.0
            # Convert the 'geometry' column from WKT to shapely polygons
            df["geometry"] = df["geometry"].apply(loads)

            # Create a GeoDataFrame with EPSG:4326 CRS (latitude/longitude)
            gdf = gpd.GeoDataFrame(df, geometry="geometry", crs="EPSG:4326")

            # Center the map based on the dataset's centroid
            center = gdf.geometry.centroid.unary_union.centroid
            map_ = folium.Map(
                location=[center.y, center.x], zoom_start=12, tiles="cartodbpositron"
            )
            gdf[BEST_MODEL] = gdf[BEST_MODEL].clip(lower=PRED_MIN, upper=PRED_MAX)
            # Create a color map based on the forest model predictions
            colormap = folium.LinearColormap(
                ["blue", "green", "yellow", "red"], vmin=PRED_MIN, vmax=PRED_MAX
            )

            # Add polygons to the map with colors representing microplastic predictions
            for _, row in gdf.iterrows():
                folium.GeoJson(
                    row["geometry"],
                    style_function=lambda feature, value=row[BEST_MODEL]: {
                        "fillColor": colormap(value),
                        "color": "black",
                        "weight": 0.5,
                        "fillOpacity": 0.7,
                    },
                    tooltip=folium.Tooltip(f"Prediction: {row[BEST_MODEL]:.4f}"),
                ).add_to(map_)

            # Add the color scale legend to the map
            colormap.caption = "Microplastic Concentration (part./m³)"
            colormap.add_to(map_)

            # Save the map to an HTML file
            map_file = os.path.join(
                *FOLDERS_DOWNLOAD_NAMES["MAIN"],
                FOLDERS_DOWNLOAD_NAMES["DATASET"],
                FILE_MAP_PREDICTIONS,
            )
            map_.save(map_file)
            logger.info(f"Map generated: {map_file}")
            return STATUS_OK, {"message": "Map saved successfully."}
        except Exception as e:
            logger.error(f"Error in show_map: {str(e)}")
            return STATUS_BAD_REQUEST, {"message": str(e)}

    def outputs_db(self):
        """
        Save the outputs to the database.
        """
        try:
            outputs_db = OutputsDB()
            output_path = os.path.join(
                *FOLDERS_DOWNLOAD_NAMES["MAIN"],
                FOLDERS_DOWNLOAD_NAMES["DATASET"],
                FILE_DATASET_WITH_PREDICTIONS,
            )

            status, message = outputs_db.insert_outputs(output_path)
            if status != STATUS_OK:
                logger.error(f"Error inserting outputs: {message}")
                return STATUS_BAD_REQUEST, {"message": str(message)}

            logger.info("Outputs inserted successfully.")
            return STATUS_OK, {"message": "Outputs inserted successfully."}
        except Exception as e:
            logger.error(f"Error in outputs_db: {str(e)}")
            return STATUS_BAD_REQUEST, {"message": str(e)}
