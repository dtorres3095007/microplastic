from fastapi import FastAPI
from src.api.trainer import trainer
from src.api.predictor import predictor
from src.api.media_collections.router import router as media_collections_router
from src.api.media_files.router import router as media_files_router
from src.api.forum.router import router as forum_router
from config import setup_logger
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles


logger = setup_logger()

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/media", StaticFiles(directory="media"), name="media")
app.include_router(trainer.router, prefix="/trainer")
app.include_router(predictor.router, prefix="/predictor")
app.include_router(
    media_collections_router, prefix="/media_collections", tags=["media_collections"]
)
app.include_router(media_files_router, prefix="/media_files", tags=["media_files"])
app.include_router(forum_router, prefix="/forum", tags=["forum"])

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="0.0.0.0", port=3000, reload=True)
