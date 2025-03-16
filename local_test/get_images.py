from datetime import date, timedelta
import json
from shapely.geometry import shape

from src.shared.constants import FOLDERS_DOWNLOAD_NAMES
from src.entities.v1.integrations.integrations import Integrations

if __name__ == "__main__":
    with open("local_test/map.geojson") as f:
        geojson_data = json.load(f)
    geom = geojson_data["features"][0]["geometry"]
    polygon = shape(geom).wkt
    today = date.today()
    end_date = today.strftime("%Y-%m-%d")
    yesterday = today - timedelta(days=1)
    initial_date = yesterday.strftime("%Y-%m-%d")
    integrations = Integrations(FOLDERS_DOWNLOAD_NAMES)
    status, message = integrations.get_images(polygon, initial_date, end_date)
    print(status, message)
