from src.entities.v1.integrations.integrations import Integrations

if __name__ == "__main__":
    lon = 0.0
    lat = 0.0
    window_size = 0
    integrations = Integrations()
    status, message = integrations.extract_area_at_coordinates(lon, lat, window_size)
    print(status, message)