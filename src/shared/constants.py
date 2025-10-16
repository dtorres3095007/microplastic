R10_BANDS = {"B02", "B03", "B04", "B08"}
R20_BANDS = {"B05", "B06", "B07", "B8A", "B11", "B12"}
BAND_BLUE = "BLUE"
BAND_GREEN = "GREEN"
BAND_RED = "RED"
BAND_REDEDGE1 = "REDEDGE1"
BAND_REDEDGE2 = "REDEDGE2"
BAND_REDEDGE3 = "REDEDGE3"
BAND_NIR_10M = "NIR_10m"
BAND_NIR_20M = "NIR_20m"
BAND_SWIR1 = "SWIR1"
BAND_SWIR2 = "SWIR2"
PRED_FOREST = 0.6

BANDS_MAP = {
    "B02": BAND_BLUE,
    "B03": BAND_GREEN,
    "B04": BAND_RED,
    "B05": BAND_REDEDGE1,
    "B06": BAND_REDEDGE2,
    "B07": BAND_REDEDGE3,
    "B08": BAND_NIR_10M,
    "B8A": BAND_NIR_20M,
    "B11": BAND_SWIR1,
    "B12": BAND_SWIR2,
}
BANDS_LIST = [
    BAND_BLUE,
    BAND_GREEN,
    BAND_RED,
    BAND_REDEDGE1,
    BAND_REDEDGE2,
    BAND_REDEDGE3,
    BAND_NIR_10M,
    BAND_NIR_20M,
    BAND_SWIR1,
    BAND_SWIR2,
]
R10_FOLDER = "R10m"
R20_FOLDER = "R20m"
STATUS_OK = 200
STATUS_ERROR = 500
STATUS_NOT_FOUND = 404
STATUS_BAD_REQUEST = 400
STATUS_UNAUTHORIZED = 401
STATUS_FORBIDDEN = 403
STATUS_CONFLICT = 409
STATUS_INTERNAL_SERVER_ERROR = 500
POLYGON_11_55_72_91 = "polygon_11.55_-72.91"
POLYGON_11_56_72_93 = "polygon_11.56_-72.93"
POLYGON_11_57_72_95 = "polygon_11.57_-72.95"
POLYGON_11_58_72_97 = "polygon_11.58_-72.97"
FEATURE_NDVI = "NDVI"
FEATURE_NDWI = "NDWI"
FEATURE_NDCI = "NDCI"
FEATURE_FDI = "FDI"
FEATURE_NDPI = "NDPI"
FEATURES_LIST = [FEATURE_NDVI, FEATURE_NDWI, FEATURE_NDCI, FEATURE_FDI, FEATURE_NDPI]
FILE_GEOJSON = "polygon.geojson"
FILE_GRID = "grid_10m.geojson"
FILE_DATASET_INDICATORS = "dataset_indicators.csv"
FILE_DATASET_WITH_PREDICTIONS = "dataset_with_predictions.csv"
BEST_MODEL = "pred_forest"
FILE_MAP_PREDICTIONS = "microplastic_predictions_map.html"
POLYGONS_MODEL_LIST = [
    POLYGON_11_55_72_91,
    POLYGON_11_56_72_93,
    POLYGON_11_57_72_95,
    POLYGON_11_58_72_97,
]
DATES_MODEL_LIST = [
    {"initial_date": "2024-12-21", "end_date": "2024-12-27"},
    {"initial_date": "2025-01-22", "end_date": "2025-01-28"},
    {"initial_date": "2025-02-22", "end_date": "2025-02-28"},
    {"initial_date": "2025-03-22", "end_date": "2025-03-28"},
    {"initial_date": "2025-04-22", "end_date": "2025-04-28"},
    {"initial_date": "2025-05-22", "end_date": "2025-05-28"},
]
FOLDERS_DOWNLOAD_NAMES = {
    "MAIN": ["data_predictor"],
    "ZIP": "download",
    "CLEANED": "processed",
    "EXTRACTED": "extracted",
    "EXTRACTED_AREA": "extracted_area",
    "FEATURES": "features",
    "FEATURES_MEAN": "features_mean",
    "BANDS_MEAN": "bands_mean",
    "POLYGONS": "polygons",
    "DATASET": "dataset",
}

FOLDER_POLYGONS = ["data_trainer", "polygons"]
FOLDERS_MODEL_NAMES = {
    "MAIN": ["data_trainer", "images"],
    "ZIP": "download",
    "CLEANED": "processed",
    "EXTRACTED": "extracted",
    "FEATURES": "features",
}

FOLDERS_DATASET_NAMES = {
    "MAIN": ["data_trainer", "train"],
    "DATASET": "dataset",
    "MODELS": "models",
}

MICROPLASTIC_DATA = [
    {
        "folder": POLYGON_11_55_72_91,
        "latitude": 11.55,
        "longitude": -72.91,
        "date": "2024-12-24",
        "microplastic_concentration": 1.85,
    },
    {
        "folder": POLYGON_11_56_72_93,
        "latitude": 11.56,
        "longitude": -72.93,
        "date": "2024-12-24",
        "microplastic_concentration": 0.70,
    },
    {
        "folder": POLYGON_11_57_72_95,
        "latitude": 11.57,
        "longitude": -72.95,
        "date": "2024-12-24",
        "microplastic_concentration": 0.48,
    },
    {
        "folder": POLYGON_11_58_72_97,
        "latitude": 11.58,
        "longitude": -72.97,
        "date": "2024-12-24",
        "microplastic_concentration": 0.42,
    },
    {
        "folder": POLYGON_11_55_72_91,
        "latitude": 11.55,
        "longitude": -72.91,
        "date": "2025-01-24",
        "microplastic_concentration": 1.76,
    },
    {
        "folder": POLYGON_11_56_72_93,
        "latitude": 11.56,
        "longitude": -72.93,
        "date": "2025-01-24",
        "microplastic_concentration": 0.69,
    },
    {
        "folder": POLYGON_11_57_72_95,
        "latitude": 11.57,
        "longitude": -72.95,
        "date": "2025-01-24",
        "microplastic_concentration": 0.38,
    },
    {
        "folder": POLYGON_11_58_72_97,
        "latitude": 11.58,
        "longitude": -72.97,
        "date": "2025-01-24",
        "microplastic_concentration": 0.48,
    },
    {
        "folder": POLYGON_11_55_72_91,
        "latitude": 11.55,
        "longitude": -72.91,
        "date": "2025-02-24",
        "microplastic_concentration": 1.61,
    },
    {
        "folder": POLYGON_11_56_72_93,
        "latitude": 11.56,
        "longitude": -72.93,
        "date": "2025-02-24",
        "microplastic_concentration": 0.65,
    },
    {
        "folder": POLYGON_11_57_72_95,
        "latitude": 11.57,
        "longitude": -72.95,
        "date": "2025-02-24",
        "microplastic_concentration": 0.51,
    },
    {
        "folder": POLYGON_11_58_72_97,
        "latitude": 11.58,
        "longitude": -72.97,
        "date": "2025-02-24",
        "microplastic_concentration": 0.46,
    },
    {
        "folder": POLYGON_11_55_72_91,
        "latitude": 11.55,
        "longitude": -72.91,
        "date": "2025-03-24",
        "microplastic_concentration": 1.53,
    },
    {
        "folder": POLYGON_11_56_72_93,
        "latitude": 11.56,
        "longitude": -72.93,
        "date": "2025-03-24",
        "microplastic_concentration": 0.69,
    },
    {
        "folder": POLYGON_11_57_72_95,
        "latitude": 11.57,
        "longitude": -72.95,
        "date": "2025-03-24",
        "microplastic_concentration": 0.32,
    },
    {
        "folder": POLYGON_11_58_72_97,
        "latitude": 11.58,
        "longitude": -72.97,
        "date": "2025-03-24",
        "microplastic_concentration": 0.44,
    },
    {
        "folder": POLYGON_11_55_72_91,
        "latitude": 11.55,
        "longitude": -72.91,
        "date": "2025-04-24",
        "microplastic_concentration": 1.95,
    },
    {
        "folder": POLYGON_11_56_72_93,
        "latitude": 11.56,
        "longitude": -72.93,
        "date": "2025-04-24",
        "microplastic_concentration": 0.60,
    },
    {
        "folder": POLYGON_11_57_72_95,
        "latitude": 11.57,
        "longitude": -72.95,
        "date": "2025-04-24",
        "microplastic_concentration": 0.40,
    },
    {
        "folder": POLYGON_11_58_72_97,
        "latitude": 11.58,
        "longitude": -72.97,
        "date": "2025-04-24",
        "microplastic_concentration": 0.42,
    },
    {
        "folder": POLYGON_11_55_72_91,
        "latitude": 11.55,
        "longitude": -72.91,
        "date": "2025-05-14",
        "microplastic_concentration": 1.73,
    },
    {
        "folder": POLYGON_11_56_72_93,
        "latitude": 11.56,
        "longitude": -72.93,
        "date": "2025-05-14",
        "microplastic_concentration": 0.58,
    },
    {
        "folder": POLYGON_11_57_72_95,
        "latitude": 11.57,
        "longitude": -72.95,
        "date": "2025-05-14",
        "microplastic_concentration": 0.44,
    },
    {
        "folder": POLYGON_11_58_72_97,
        "latitude": 11.58,
        "longitude": -72.97,
        "date": "2025-05-14",
        "microplastic_concentration": 0.47,
    },
]
