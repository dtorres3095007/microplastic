from src.entities.v1.integrations.integrations import Integrations


def lambda_handler(lon: float, lat: float, window_size: int):
    integrations = Integrations()
    status, message = integrations.extract_area_at_coordinates(lon, lat, window_size)
    return status, message
