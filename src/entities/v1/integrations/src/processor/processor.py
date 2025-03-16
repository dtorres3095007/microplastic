import numpy as np
import rasterio
from pathlib import Path
from rasterio.plot import show
import matplotlib.pyplot as plt
import rasterio.env
from rasterio.transform import rowcol
from rasterio.warp import calculate_default_transform, reproject, Resampling

from src.shared.constants import STATUS_INTERNAL_SERVER_ERROR, STATUS_OK


class Processor:
    def __init__(self, threshold=10000):
        self.threshold = threshold

        # Función para leer una banda de Sentinel-2

    def read_band(self, file_path: str):
        """Lee una banda raster de un archivo .jp2 o .tif"""
        with rasterio.open(file_path) as dataset:
            band = dataset.read(1)  # Leer la primera capa de la banda
            profile = dataset.profile  # Obtener los metadatos
        return band, profile

    def find_subfolder(self, parent_folder, subfolder_name):
        """Read the first band layer from the dataset."""
        parent_path = Path(parent_folder)
        for subfolder in parent_path.rglob(subfolder_name):
            if subfolder.is_dir():
                return subfolder
        return None

    def clean_problematic_areas(self, band):
        """
        Clean problematic areas in the data band using a threshold value.
        Areas with problematic values are set to NaN.
        """
        # Create a mask for problematic areas
        mask_problematic = band > self.threshold  # Define a threshold value (adjustable as needed)
        # Clean the problematic areas
        band_cleaned = np.where(mask_problematic, np.nan, band)
        return band_cleaned

    def save_cleaned_band(self, band, profile, output_path: str):
        """Save a cleaned band to a .tif file ensuring CRS is preserved."""
        
        # Verificar si CRS y Transform están en el perfil
        if profile.get("crs") is None:
            profile["crs"] = rasterio.crs.CRS.from_epsg(32618)  # Forzar CRS si está ausente

        if profile.get("transform") is None:
            raise ValueError("❌ Transform is missing! The image might not be correctly georeferenced.")

        profile.update(
            dtype=rasterio.uint16, 
            count=1, 
            nodata=0,
            driver="GTiff"
        )

        band_cleaned = np.where(np.isnan(band), 0, band).astype(rasterio.uint16)

        with rasterio.open(output_path, "w", **profile) as dst:
            dst.write(band_cleaned, 1)
            dst.crs = profile["crs"]

    def visualize_band(self, image_path: str, output_folder: str):
        print(f"Visualizing the band: {image_path}")
        try:
            with rasterio.open(image_path) as src:
                # Read the first band (you can adjust if you have more than one band)
                band = src.read(1)
                # Create a matplotlib figure to display the image
                plt.figure(figsize=(10, 10))
                # Display the image with a color map (cmap)
                plt.imshow(band, cmap="gray")  # You can change 'cmap' if you want a different color
                # Add a title
                plt.title("Band Visualization")
                print(f"Visualizing the band: {image_path}")
                # Save the image
                plt.savefig(output_folder)
        except rasterio.errors.RasterioIOError as e:
            print(f"Error opening the file: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

    def extract_area_at_coordinates(
        self, image_path: str, lon: float, lat: float, window_size: int, output_path: str
    ):
        """
        Extract an area around specified coordinates from a raster image and save it as a new image.

        Parameters:
        - image_path: str, path to the .jp2 image file.
        - lon: float, longitude coordinate.
        - lat: float, latitude coordinate.
        - window_size: int, size of the square area to extract (in pixels).
        - output_path: str, path to save the new image.

        Returns:
        - None
        """
        try:
            with rasterio.open(image_path) as src:
                # Convert the coordinates to row and column indices
                row, col = rowcol(src.transform, lon, lat)

                # Calculate the window to extract
                half_window = window_size // 2
                window = (
                    (row - half_window, row + half_window),
                    (col - half_window, col + half_window),
                )

                # Read the window from the image
                band = src.read(1, window=window)  # Read the specified window
                transform = src.window_transform(window)  # Get the transform for the window

                # Save the extracted area as a new image
                profile = src.profile
                profile.update(
                    {"height": band.shape[0], "width": band.shape[1], "transform": transform},
                    GDAL_TIFF_INTERNAL_MASK="YES",
                )
                with rasterio.Env(GDAL_PAM_ENABLED="NO"):
                    with rasterio.open(output_path, "w", **profile) as dst:
                        dst.write(band, 1)
        except Exception as e:
            print(f"An error occurred: {e}")
        print(f"Extracted area saved to: {output_path}")

    def rescale_band(self, band, profile, target_resolution):
        """Rescale the band to the target resolution (10m or 20m)."""
        original_transform = profile["transform"]
        left, bottom, right, top = rasterio.transform.array_bounds(
            profile["height"], profile["width"], profile["transform"]
        )

        dst_transform, width, height = calculate_default_transform(
            profile["crs"], profile["crs"], width=profile["width"], height=profile["height"],
            left=left, bottom=bottom, right=right, top=top, resolution=target_resolution
        )

        
        profile.update(transform=dst_transform, width=width, height=height)

        rescaled_band = np.empty((height, width), dtype=rasterio.uint16)
        reproject(
            source=band,
            destination=rescaled_band,
            src_transform=original_transform,
            src_crs=profile["crs"],
            dst_transform=dst_transform,
            dst_crs=profile["crs"],
            resampling=Resampling.bilinear
        )

        return rescaled_band, profile