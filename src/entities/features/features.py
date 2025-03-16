import numpy as np
import rasterio
import os
from src.shared.constants import (
    FEATURE_FDI,
    FEATURE_NDCI,
    FEATURE_NDPI,
    FEATURE_NDWI,
    FEATURE_NDVI,
    STATUS_BAD_REQUEST,
    STATUS_INTERNAL_SERVER_ERROR,
    STATUS_OK,
)


class Feature:
    def __init__(self, path_bands, output_path):
        """
        Initialize the Feature class.
        :param bands: Dictionary containing band file paths.
        :param output_path: Path to store the processed results.
        """
        self.path_bands = path_bands
        self.output_path = output_path
        self.bands = {}

    def open_bands(self):
        """
        Open the bands using rasterio.
        """
        USING_BANDS_NAMES = ["RED", "GREEN", "NIR_10m", "SWIR1", "REDEDGE1"]
        status = STATUS_OK
        message = ""
        for band_name, band_path in self.path_bands.items():
            if band_name not in USING_BANDS_NAMES:
                continue
            try:
                with rasterio.open(band_path) as src:
                    band = src.read(1).astype(np.float32)  # Read band data as float32
                    self.bands[band_name] = band
            except Exception as e:
                status = STATUS_INTERNAL_SERVER_ERROR
                message = f"Error opening band {band_name}: {str(e)}"

        return status, message

    def calculate_ndvi(self):
        """
        Calculate the Normalized Difference Vegetation Index (NDVI).
        """
        try:
            red = self.bands.get("RED")
            nir = self.bands.get("NIR_10m")
            if red is None or nir is None:
                return STATUS_BAD_REQUEST, {"message": "Missing required bands for NDVI."}

            ndvi = (nir - red) / (nir + red + 1e-10)  # Calculate NDVI
            status, message = self.save_feature(ndvi, f"{FEATURE_NDVI}.tif")
            return status, message
        except Exception as e:
            return STATUS_INTERNAL_SERVER_ERROR, {"message": f"Error in NDVI: {str(e)}"}

    def calculate_ndwi(self):
        """
        Calculate Normalized Difference Water Index (NDWI).
        """
        try:
            green = self.bands.get("GREEN")
            nir = self.bands.get("NIR_10m")
            if green is None or nir is None:
                return STATUS_BAD_REQUEST, {"message": "Missing required bands for NDWI."}

            ndwi = (green - nir) / (green + nir + 1e-10)  # Calculate NDWI
            status, message = self.save_feature(ndwi, f"{FEATURE_NDWI}.tif")
            return status, message
        except Exception as e:
            return STATUS_INTERNAL_SERVER_ERROR, {"message": f"Error in NDWI: {str(e)}"}

    def calculate_ndci(self):
        """
        Calculate Normalized Difference Chlorophyll Index (NDCI).
        """
        try:
            rededge1 = self.bands.get("REDEDGE1")
            red = self.bands.get("RED")
            if rededge1 is None or red is None:
                return STATUS_BAD_REQUEST, {"message": "Missing required bands for NDCI."}

            ndci = (rededge1 - red) / (rededge1 + red + 1e-10)  # Calculate NDCI
            status, message = self.save_feature(ndci, f"{FEATURE_NDCI}.tif")
            return status, message
        except Exception as e:
            return STATUS_INTERNAL_SERVER_ERROR, {"message": f"Error in NDCI: {str(e)}"}

    def calculate_fdi(self):
        """
        Calculate Fire Detection Index (FDI).
        """
        try:
            swir1 = self.bands.get("SWIR1")
            nir = self.bands.get("NIR_10m")
            if swir1 is None or nir is None:
                return STATUS_BAD_REQUEST, {"message": "Missing required bands for FDI."}

            fdi = swir1 - nir  # Calculate FDI
            status, message = self.save_feature(fdi, f"{FEATURE_FDI}.tif")
            return status, message
        except Exception as e:
            return STATUS_INTERNAL_SERVER_ERROR, {"message": f"Error in FDI: {str(e)}"}

    def calculate_ndpi(self):
        """
        Calculate Normalized Difference Pigment Index (NDPI).
        """
        try:
            red = self.bands.get("RED")
            swir1 = self.bands.get("SWIR1")
            if red is None or swir1 is None:
                return STATUS_BAD_REQUEST, {"message": "Missing required bands for NDPI."}

            ndpi = (red - swir1) / (red + swir1 + 1e-10)  # Calculate NDPI
            status, message = self.save_feature(ndpi, f"{FEATURE_NDPI}.tif")
            return status, message
        except Exception as e:
            return STATUS_INTERNAL_SERVER_ERROR, {"message": f"Error in NDPI: {str(e)}"}

    def save_feature(self, feature_array, filename):
        """
        Save the calculated feature to a file.
        """
        try:
            output_path = os.path.join(self.output_path, filename)
            sample_band = next(iter(self.path_bands.values()))  # Get a sample band for profile

            with rasterio.open(sample_band) as src:
                profile = src.profile

            profile.update(
                dtype=rasterio.uint16,  # Update profile to use uint16
                count=1,
                nodata=0,
                driver="GTiff"
            )
            # Scale feature to uint16
            scaled_feature = ((feature_array + 1) * 32767.5).astype(np.uint16)

            with rasterio.open(output_path, "w", **profile) as dst:
                dst.write(scaled_feature, 1)  # Write the feature to file
                dst.crs = profile["crs"]

            return STATUS_OK, {"message": f"Feature {filename} saved."}

        except Exception as e:
            return STATUS_INTERNAL_SERVER_ERROR, {"message": f"Error saving feature: {str(e)}"}
