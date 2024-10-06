from src.entities.v1.integrations.integrations import Integrations

def lambda_handler(polygon: str, initial_date: str, end_date: str):
    integrations = Integrations()
    status, message = integrations.get_images(polygon, initial_date, end_date)
    return status, message
