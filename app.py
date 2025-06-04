from fastapi import FastAPI
from src.request.trainer import trainer
from src.request.predictor import predictor
from config import setup_logger

logger = setup_logger()

app = FastAPI()

app.include_router(trainer.router, prefix="/trainer")
app.include_router(predictor.router, prefix="/predictor")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=3000, reload=True)
