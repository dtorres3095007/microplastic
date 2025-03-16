
import os
from src.api.integrations.integrations import Integrations

if __name__ == "__main__":
    input_dir = os.path.join(os.getcwd(), "downloads", "extracted_area")
    output_dir = os.path.join(os.getcwd(), "downloads", "visualized_coordinates")
    integrations = Integrations()
    status, message = integrations.visualize_images(input_dir, output_dir)
    print(status, message)
