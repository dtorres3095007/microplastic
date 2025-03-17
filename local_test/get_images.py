
from shapely.geometry import shape

from config import setup_logger
from src.api.predictor.predictor import Predictor
import geopandas as gpd

data = {
    "initial_date": "2025-03-15",
    "end_date": "2025-03-16",
    "location": {
        "coordinates": [
            [
                [
                    -73.35831397455212,
                    11.886251690628882
                ],
                [
                    -73.35831397455212,
                    11.884186337143731
                ],
                [
                    -73.35651477436537,
                    11.884186337143731
                ],
                [
                    -73.35651477436537,
                    11.886251690628882
                ],
                [
                    -73.35831397455212,
                    11.886251690628882
                ]
            ]
        ],
        "type": "Polygon"
    }
}

if __name__ == "__main__":
    logger = setup_logger()

    end_date = data["end_date"]
    location = data["location"]
    initial_date = data["initial_date"]
    polygon = shape(location).wkt
    predictor = Predictor(polygon, location.get("coordinates"), initial_date, end_date)
    # status, message = predictor.get_polygon_images()
    # status, message = predictor.calculate_features()
    # status, message = predictor.feature_mean()
    # status, message = predictor.create_polygons()
    status, message = predictor.create_dataset()

    print(status, message)
