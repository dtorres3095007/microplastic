from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from src.shared.constants import STATUS_BAD_REQUEST, STATUS_OK
from src.entities.machine_learning.trainer import Trainer
from src.api.trainer.docs import trainer_summary, trainer_description, trainer_response_description
import logging

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get(
    "/model",
    summary=trainer_summary,
    description=trainer_description,
    response_description=trainer_response_description
)
def trainer_request():
    try:
        logger.info("----- Starting TrainerRequest -----")
        trainer = Trainer()

        for step in [
            trainer.get_model_images,
            trainer.clean_model_images,
            trainer.calculate_features,
            trainer.create_dataset,
            trainer.train_models,
        ]:
            status, message = step()
            if status != STATUS_OK:
                raise HTTPException(status_code=status, detail=message)

        logger.info("Training completed successfully.")
        return JSONResponse(status_code=200, content=message)

    except Exception as e:
        logger.error(f"Unhandled error in TrainerRequest: {e}")
        raise HTTPException(
            status_code=STATUS_BAD_REQUEST,
            detail=f"Training pipeline error: {e}"
        )
