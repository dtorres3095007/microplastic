from src.entities.v1.data.data import Data
from local_test.config import setup_logger


if __name__ == "__main__":
    logger = setup_logger()
    data = Data()
    # status, message = data.get_model_images()
    # print(status, message)
    # status, message = data.clean_model_images()
    # print(status, message)
    # status, message = data.calculate_features()
    # print(status, message)
    # status, message = data.create_dataset()
    # print(status, message)
    # status, message = data.train_models()
    # print(status, message)
    status, message = data.evaluate_models()
    print(status, message)
