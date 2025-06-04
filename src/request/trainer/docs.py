# docs/trainer_docs.py

trainer_summary = "Train microplastic prediction model"

trainer_description = (
    "Executes the training pipeline using a pre-built dataset with known sampling points.\n\n"
    "**Steps executed:**\n"
    "1. Validates dataset availability\n"
    "2. Cleans and prepares satellite image data\n"
    "3. Extracts relevant indicators (NDVI, NDWI, NDCI, FDI, NDPI)\n"
    "4. Builds the dataset for training\n"
    "5. Trains the machine learning models and returns results"
)

trainer_response_description = "Training pipeline execution summary including model performance or error info"
