from api.integrationsApi import IntegrationsApi
from flask import Flask
from flask_restful import Api
import logging

logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
api = Api(app)

api.add_resource(IntegrationsApi, "/images")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
