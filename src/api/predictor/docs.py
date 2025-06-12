# src/api/predictor/docs.py

summary_microplastic = "Run full Sentinel-2 image processing and microplastic prediction pipeline"

description_microplastic = (
    "Receives a GeoJSON polygon and a date range. "
    "Downloads Sentinel-2 satellite images for the area and dates, processes them, "
    "and performs prediction using a pre-trained model."
)

response_description_microplastic = "Returns processing results or prediction output"
