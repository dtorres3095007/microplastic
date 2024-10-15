from src.api.integrations.get_visualize_image import lambda_handler
from shapely.geometry import shape
import os

if __name__ == "__main__":
    input_dir = os.path.join(os.getcwd(), "downloads", "cleaned")
    output_dir = os.path.join(os.getcwd(), "downloads", "visualized")
    lambda_handler(input_dir, output_dir)
