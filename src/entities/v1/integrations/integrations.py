from .src.copernicus.copernicus import Copernicus
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
    
    def get_images(self, polygon: str, initial_date: str, end_date: str)->dict:
        """
        Save images from the Copernicus API.
        """
        copernicus = self.copernicus()
        results = copernicus.search(polygon, initial_date, end_date)
        if not results:
            return 500, {"message": "Error in search"}
        
        results_transform = pd.DataFrame.from_dict(results["value"])
        output_folder = os.path.join(os.getcwd(), "downloads", "images")
        os.makedirs(output_folder, exist_ok=True) 
        if results_transform.shape[0] > 0 :
            results_transform["geometry"] = results_transform["GeoFootprint"].apply(shape)
            # Convert pandas dataframe to Geopandas dataframe by setting up geometry
            productDF = gpd.GeoDataFrame(results_transform).set_geometry("geometry") 
            # Remove L1C dataset if not needed
            productDF = productDF[~productDF["Name"].str.contains("L1C")] 
            print(f" total L2A tiles found {len(productDF)}")
            productDF["identifier"] = productDF["Name"].str.split(".").str[0]
            totalImages = len(productDF)
            if totalImages == 0: # If L2A tiles are not available in current query
                print(f"No tiles found")
            else: # If L2A tiles are available in current query
                # download all tiles from server
                for index,feat in productDF.iterrows():
                    print(f"Downloading {index} of {totalImages}")
                    copernicus.download(feat['Id'], feat['identifier'], output_folder)
        return 200, {"message": "Images downloaded successfully."}