import re
import os
import pandas as pd
from src.shared.constants import BANDS_MAP
from datetime import datetime
import pandas as pd


def get_band_name(filename):
    """Extracts the band name from the filename."""
    match = re.search(r"_B(\d{1,2}A?)_", filename)
    if match:
        band_code = f"B{match.group(1)}"
        return BANDS_MAP.get(band_code, band_code)
    return None


def save_dataset_to_csv(data, folder="downloads/datasets", file_name="microplastics"):
    """
    Saves the dataset as a CSV file in the specified directory.

    :param data: List of dictionaries containing the data
    :param folder: Folder where the file will be saved (default is the current directory)
    :param file_name: Name of the CSV file (default is microplastics_dataset.csv)
    """
    try:
        # Ensure the directory exists
        os.makedirs(folder, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f"{file_name}.csv"

        # Create the full file path
        folder_file = os.path.join(folder, file_name)

        # Convert the list of dictionaries into a DataFrame and save it as a CSV file
        df = pd.DataFrame(data)
        df.to_csv(folder_file, index=False)
        return True, f"Dataset saved as {folder_file}"
    except Exception as e:
        return False, str(e)
