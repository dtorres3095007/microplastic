R10_BANDS = {"B02", "B03", "B04", "B08"}
R20_BANDS = {"B05", "B06", "B07", "B8A", "B11", "B12"}
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
POLYGONS_MODEL_LIST = ["polygon_11.55_-72.91.json", "polygon_11.56_-72.93.json" , "polygon_11.57_-72-95.json" , "polygon_11.58_-72.97.json"]
DATES_MODEL_LIST = [{
        "initial_date": "2024-12-20",
        "end_date": "2024-12-27"
    },
    {
        "initial_date": "2025-01-20",
        "end_date": "2025-01-29"
    },
    {
        "initial_date": "2025-02-20",
        "end_date": "2025-02-28"
    }
]
FOLDERS_DOWNLOAD_NAMES = {
    "MAIN": ["download"],
    "ZIP": "zip",
    "CLEANED": "cleaned",
    "EXTRACTED": "extracted",
    "EXTRACTED_AREA": "extracted_area",
}
FOLDERS_MODEL_NAMES = {
    "MAIN": ["src", "shared", "model_images"],
    "ZIP": "zip",
    "CLEANED": "cleaned",
    "EXTRACTED": "extracted",
}

