from math import log
from src.entities.v1.data.data import Data
from local_test.config import setup_logger

if __name__ == "__main__":
    logger = setup_logger()
    data = Data()
    # status, message = data.get_model_images()
    status, message = data.clean_model_images()
    print(status, message)

