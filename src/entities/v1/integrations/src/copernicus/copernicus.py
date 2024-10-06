import requests
from dotenv import load_dotenv
from .constants import URL_AUTH, URL_DATA, DATA_COLLECTION
import os

class Copernicus:
    def __init__(self):
        """
        Initialize the Copernicus class.
        Loads environment variables for authentication.
        """
        # Load environment variables
        load_dotenv()
        self.user = os.getenv("COPERNICUS_USER")
        self.password = os.getenv("COPERNICUS_PASSWORD")
        self.url_auth = URL_AUTH
        self.url_data = URL_DATA
        self.data_collection = DATA_COLLECTION

    def authenticate(self) -> str:
        data = {
            "client_id": "cdse-public",
            "username": self.user,
            "password": self.password,
            "grant_type": "password",
        }
        try:
            r = requests.post(
                self.url_auth,
                data=data,
            )
            r.raise_for_status()
        except Exception as e:
            raise Exception(
                f"authenticate token creation failed. Response from the server was: {e}"
            )
        return r.json()["access_token"]

    def search(self, polygon: str, initial_date: str, end_date: str) -> dict:
        """
        Search for products in the Copernicus API.

        :param query: The search query string.
        :return: JSON response of the search results or None if an error occurs.
        """
        search_url = f"{self.url_data}?$filter=Collection/Name eq '{self.data_collection}' and OData.CSC.Intersects(area=geography'SRID=4326;{polygon}') and ContentDate/Start gt {initial_date}T00:00:00.000Z and ContentDate/Start lt {end_date}T00:00:00.000Z&$count=True&$top=1000"
        response = requests.get(search_url)
        if response.status_code == 200:
            return response.json()
        else:
            return None

    def download(self, product_id, identifier, output_folder="downloads"):
        """
        Download a specific product.

        :param product_id: The ID of the product to download.
        :param output_folder: The folder where the downloaded product will be saved.
        """
        try:
            token = self.authenticate()
            # Create requests session 
            session = requests.Session()
            # Get access token based on username and password
            session.headers.update({"Authorization": f"Bearer {token}"})
            url = f"{self.url_data}({product_id})/$value"
            response = session.get(url, allow_redirects=False)
            while response.status_code in (301, 302, 303, 307):
                url = response.headers["Location"]
                response = session.get(url, allow_redirects=False)
            file = session.get(url, verify=False, allow_redirects=True)
            with open(
                os.path.join(output_folder, f"{identifier}.zip"),
                "wb",
            ) as p:
                p.write(file.content)
        except Exception as e:
            raise Exception(
                f"Error download {identifier}: {e}"
            )

  