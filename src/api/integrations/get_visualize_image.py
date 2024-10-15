from src.entities.v1.integrations.integrations import Integrations


def lambda_handler(input_dir: str, output_dir: str):
    integrations = Integrations()
    status, message = integrations.visualize_images(input_dir, output_dir)
    return status, message
