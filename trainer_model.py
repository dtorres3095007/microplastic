from src.entities.machine_learning.trainer import Trainer
from src.shared.constants import STATUS_BAD_REQUEST, STATUS_OK
from config import setup_logger


def trainer_request():
    logger = setup_logger()

    try:
        logger.info("----- Starting TrainerRequest -----")
        trainer = Trainer()

        for step in [
            # trainer.get_model_images,
            # trainer.clean_model_images,
            # trainer.calculate_features,
            # trainer.create_dataset,
            # trainer.train_models,
            trainer.evaluate_models,
        ]:
            status, message = step()
            if status != STATUS_OK:
                logger.error(f"Step failed with status {status}: {message}")
                return status, message

        logger.info("Training completed successfully.")
        return STATUS_OK, "Training completed successfully."

    except Exception as e:
        logger.error(f"Unhandled error in TrainerRequest: {e}")
        return STATUS_BAD_REQUEST, f"Training pipeline error: {e}"


if __name__ == "__main__":
    resp = trainer_request()
    print(resp)
