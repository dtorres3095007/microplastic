
from shapely.geometry import shape
from src.shared.constants import STATUS_OK, STATUS_BAD_REQUEST
from src.entities.machine_learning.predictor import Predictor
from config import setup_logger

data = {
    "initial_date": "2025-06-01",
    "end_date": "2025-06-30",
    "location": {
        "coordinates": [
            [
                [
                    -72.94475726112186,
                    11.537126610927615
                ],
                [
                    -72.90527514442265,
                    11.55764540798314
                ],
                [
                    -72.91231326087772,
                    11.570595022989117
                ],
                [
                    -72.95042208656132,
                    11.549908988703729
                ],
                [
                    -72.94475726112186,
                    11.537126610927615
                ]
            ]
        ],
        "type": "Polygon"
    }
}


def predictor_request():
    logger = setup_logger()

    try:
        polygon_wkt = shape(data["location"]).wkt
        logger.info(f"initial_date : {data['initial_date']} - end_date : {data['end_date']}")

        predictor = Predictor(
            polygon_wkt,
            data["location"]["coordinates"],
            data["initial_date"],
            data["end_date"]
        )

        for step in [
            predictor.clean_folders,
            predictor.get_polygon_images,
            predictor.calculate_features,
            predictor.feature_mean,
            predictor.bands_means,
            predictor.create_polygons,
            predictor.create_dataset,
            predictor.predict,
            predictor.show_map,
        ]:
            status, message = step()
            if status != STATUS_OK:
                logger.error(f"Step failed with status {status}: {message}")
                return STATUS_OK, "Training completed successfully."

        logger.info("Predictor completed successfully.")
        return STATUS_OK, "Training completed successfully."

    except Exception as e:
        logger.error(f"Error in post PredictorRequest: {e}")
        return STATUS_BAD_REQUEST, f"predictor pipeline error: {e}"


if __name__ == "__main__":
    resp = predictor_request()
    print(resp)
