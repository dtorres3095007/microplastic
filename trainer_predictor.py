from shapely.geometry import shape
from src.shared.constants import STATUS_OK, STATUS_BAD_REQUEST
from src.entities.machine_learning.predictor import Predictor
from config import setup_logger
from datetime import datetime, timedelta


def get_month_date_range():
    """Return first and last date of the current month in YYYY-MM-DD format."""
    today = datetime.today()

    first_day = today.replace(day=1).strftime("%Y-%m-%d")

    next_month = today.replace(day=28) + timedelta(days=4)
    last_day = (next_month.replace(day=1) - timedelta(days=1)).strftime("%Y-%m-%d")

    return first_day, last_day


def predictor_request():
    logger = setup_logger()

    try:
        initial_date, end_date = get_month_date_range()

        polygon = {
            "coordinates": [
                [
                    [-72.94475726112186, 11.537126610927615],
                    [-72.90527514442265, 11.55764540798314],
                    [-72.91231326087772, 11.570595022989117],
                    [-72.95042208656132, 11.549908988703729],
                    [-72.94475726112186, 11.537126610927615],
                ]
            ],
            "type": "Polygon",
        }

        polygon_wkt = shape(polygon).wkt

        logger.info(f"initial_date : {initial_date} - end_date : {end_date}")

        predictor = Predictor(
            polygon_wkt,
            polygon["coordinates"],
            initial_date,
            end_date,
        )

        for step in [
            # predictor.clean_folders,
            # predictor.get_polygon_images,
            predictor.calculate_features,
            # predictor.feature_mean,
            # predictor.bands_means,
            # predictor.create_polygons,
            # predictor.create_dataset,
            # predictor.predict,
            # predictor.show_map,
            # predictor.outputs_db,
        ]:
            status, message = step()
            if status != STATUS_OK:
                logger.error(f"Step failed with status {status}: {message}")
                return STATUS_OK, "Training failed."

        logger.info("Predictor completed successfully.")
        return STATUS_OK, "Training completed successfully."

    except Exception as e:
        logger.error(f"Error in post PredictorRequest: {e}")
        return STATUS_BAD_REQUEST, f"predictor pipeline error: {e}"


if __name__ == "__main__":
    resp = predictor_request()
    print(resp)
