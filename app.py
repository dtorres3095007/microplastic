from src.request.trainer.trainer import TrainerRequest
from src.request.predictor.predictor import PredictorRequest
from flask import Flask
from flask_restful import Api
from config import setup_logger

logger = setup_logger()

app = Flask(__name__)
api = Api(app)

api.add_resource(TrainerRequest, "/trainer")
api.add_resource(PredictorRequest, "/predictor")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)
