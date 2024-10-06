from src.api.integrations.get_images import lambda_handler
from datetime import date, timedelta
import json
from shapely.geometry import shape

if __name__ == "__main__":
    with open('local_test/map.geojson') as f:
        geojson_data = json.load(f)
    geom = geojson_data['features'][0]['geometry']
    polygon = shape(geom).wkt
    today =  date.today()
    end_date = today.strftime("%Y-%m-%d")
    yesterday = today - timedelta(days=5)
    initial_date = yesterday.strftime("%Y-%m-%d")
    lambda_handler(polygon, initial_date, end_date)