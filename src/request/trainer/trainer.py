from flask_restful import Resource
from src.shared.constants import STATUS_BAD_REQUEST, STATUS_OK
from src.api.trainer.trainer import Trainer

import logging

logger = logging.getLogger(__name__)


class TrainerRequest(Resource):
    def get(self):
        try:
            logger.info("----- Request TrainerRequest -----")
            trainer = Trainer()
            status, message = trainer.get_model_images()

            if status != STATUS_OK:
                return message, status

            status, message = trainer.clean_model_images()

            if status != STATUS_OK:
                return message, status

            status, message = trainer.calculate_features()
            if status != STATUS_OK:
                return message, status

            status, message = trainer.create_dataset()
            if status != STATUS_OK:
                return message, status

            status, message = trainer.train_models()
            return message, status

        except Exception as e:
            logger.error(f"Error in TrainerRequest: {e}")
            return {"message": f"Data model error : {e}"}, STATUS_BAD_REQUEST
