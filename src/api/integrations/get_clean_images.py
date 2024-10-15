from src.entities.v1.integrations.integrations import Integrations


def lambda_handler():
    integrations = Integrations()
    status, message = integrations.clean_images()
    return status, message
