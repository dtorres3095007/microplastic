from src.request.data.data import DataRequest
from src.request.integrations.integrations import IntegrationsRequest
from flask import Flask
from flask_restful import Api
from config import setup_logger

logger = setup_logger()

app = Flask(__name__)
api = Api(app)

api.add_resource(DataRequest, "/model/train")
api.add_resource(IntegrationsRequest, "/images")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)
