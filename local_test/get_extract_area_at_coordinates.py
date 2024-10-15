from src.api.integrations.get_extract_area_at_coordinates import lambda_handler

if __name__ == "__main__":
    lon = -72.94414177751337
    lat = 112.094306897221088
    window_size = 100
    lambda_handler(lon, lat, window_size)
