from flask_restful import Resource
from src.shared.constants import STATUS_BAD_REQUEST, STATUS_OK
from src.api.data.data import Data

import logging

logger = logging.getLogger(__name__)


class DataRequest(Resource):
    def get(self):
        try:
            logger.info("----- Request DataRequest -----")
            data = Data()
            status, message = data.get_model_images()

            if status != STATUS_OK:
                return message, status

            status, message = data.clean_model_images()

            if status != STATUS_OK:
                return message, status

            status, message = data.calculate_features()
            if status != STATUS_OK:
                return message, status

            status, message = data.create_dataset()
            if status != STATUS_OK:
                return message, status

            status, message = data.train_models()
            return message, status

        except Exception as e:
            logger.error(f"Error in DataRequest: {e}")
            return {"message": f"Data model error : {e}"}, STATUS_BAD_REQUEST
