import os
from src.entities.v1.integrations.integrations import Integrations

if __name__ == "__main__":
    input_dir = os.path.join(os.getcwd(), "downloads", "cleaned")
    output_dir = os.path.join(os.getcwd(), "downloads", "visualized")
    integrations = Integrations()
    status, message = integrations.visualize_images(input_dir, output_dir)
    print(status, message)
