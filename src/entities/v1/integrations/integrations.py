from .src.copernicus.copernicus import Copernicus
from .src.processor.processor import Processor
import pandas as pd
import geopandas as gpd
import os
from shapely.geometry import shape


class Integrations:
    def __init__(self):
        """
        Initialize the integrations class.
        """
        self.copernicus = Copernicus
        self.processor = Processor

    def get_images(self, polygon: str, initial_date: str, end_date: str) -> dict:
        """
        Save images from the Copernicus API.
        """
        copernicus = self.copernicus()
        results = copernicus.search(polygon, initial_date, end_date)
        if not results:
            return 500, {"message": "Error in search"}

        results_transform = pd.DataFrame.from_dict(results["value"])
        output_folder = os.path.join(os.getcwd(), "downloads", "zip")
        os.makedirs(output_folder, exist_ok=True)
        if results_transform.shape[0] > 0:
            results_transform["geometry"] = results_transform["GeoFootprint"].apply(shape)
            # Convert pandas dataframe to Geopandas dataframe by setting up geometry
            productDF = gpd.GeoDataFrame(results_transform).set_geometry("geometry")
            # Remove L1C dataset if not needed
            productDF = productDF[~productDF["Name"].str.contains("L1C")]
            print(f"total L2A tiles found {len(productDF)}")
            productDF["identifier"] = productDF["Name"].str.split(".").str[0]
            totalImages = len(productDF)
            if totalImages == 0:  # If L2A tiles are not available in current query
                print(f"No tiles found")
            else:  # If L2A tiles are available in current query
                # download all tiles from server
                for index, feat in productDF.iterrows():
                    print(f"Downloading {index} of {totalImages}")
                    # copernicus.download(feat["Id"], feat["identifier"], output_folder)
            # Extract all the zip files
            print("Extracting zip files...")
            for file in os.listdir(output_folder):
                if file.endswith(".zip"):
                    copernicus.extract_zip(
                        os.path.join(output_folder, file),
                        os.path.join(os.getcwd(), "downloads", "extracted"),
                    )
                    copernicus.delete_file(os.path.join(output_folder, file))
        return 200, {"message": "Images downloaded successfully."}

    def clean_images(self):
        """Process files in the img_data folder and clean them of problematic areas."""
        input_dir = os.path.join(os.getcwd(), "downloads", "extracted")
        output_dir = os.path.join(os.getcwd(), "downloads", "cleaned")
        try:
            processor = self.processor(threshold=10000)
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)

            for subfolder in os.listdir(input_dir):
                subfolder_path = os.path.join(input_dir, subfolder)
                if os.path.isdir(subfolder_path):
                    images = processor.find_subfolder(subfolder_path, "R10m")
                    if images:
                        for filename in os.listdir(images):
                            if filename.endswith(".jp2"):  # Change to .tif if that is the format
                                file_path = os.path.join(images, filename)
                                print(f"Processing file: {file_path}")
                                # Read the data band
                                band, profile = processor.read_band(file_path)
                                # Clean the problematic areas
                                band_cleaned = processor.clean_problematic_areas(band)
                                # Save the cleaned band
                                folder = os.path.join(output_dir, subfolder)
                                if not os.path.exists(folder):
                                    os.makedirs(folder)
                                output_path = os.path.join(
                                    folder,
                                    filename.replace(".jp2", ".tif"),
                                )
                                processor.save_cleaned_band(band_cleaned, profile, output_path)
        except Exception as e:
            print(f"An error occurred: {e}")
            return 500, {"message": "An error occurred."}
        return 200, {"message": "Images cleaned successfully."}

    def visualize_images(self, input_dir: str, output_dir: str):
        """Visualize the cleaned images."""
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        try:
            processor = self.processor()
            for subfolder in os.listdir(input_dir):
                subfolder_path = os.path.join(input_dir, subfolder)
                if os.path.isdir(subfolder_path):
                    for filename in os.listdir(subfolder_path):
                        if filename.endswith(".tif"):
                            folder = os.path.join(output_dir, subfolder)
                            if not os.path.exists(folder):
                                os.makedirs(folder)
                            clean_filename = filename.replace(".tif", "")
                            folder = os.path.join(folder, clean_filename)
                            image_path = os.path.join(subfolder_path, filename)
                            processor.visualize_band(image_path, folder)
        except Exception as e:
            print(f"An error occurred: {e}")
            return 500, {"message": "An error occurred."}
        return 200, {"message": "Images visualized successfully."}

    def extract_area_at_coordinates(self, lon: float, lat: float, window_size: int):
        """Extract an area around specified coordinates from a raster image and save it as a new image."""
        input_dir = os.path.join(os.getcwd(), "downloads", "cleaned")
        output_dir = os.path.join(os.getcwd(), "downloads", "extracted_area")
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        try:
            processor = self.processor()
            for subfolder in os.listdir(input_dir):
                subfolder_path = os.path.join(input_dir, subfolder)
                if os.path.isdir(subfolder_path):
                    for filename in os.listdir(subfolder_path):
                        if filename.endswith(".tif"):
                            folder = os.path.join(output_dir, subfolder)
                            if not os.path.exists(folder):
                                os.makedirs(folder)
                            output_path = os.path.join(folder, filename)
                            image_path = os.path.join(subfolder_path, filename)
                            processor.extract_area_at_coordinates(
                                image_path, lon, lat, window_size, output_path
                            )
        except Exception as e:
            print(f"An error occurred: {e}")
            return 500, {"message": "An error occurred."}
        return 200, {"message": "Images extracted successfully."}
