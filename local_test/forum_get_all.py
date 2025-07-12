from dotenv import load_dotenv
import os
import requests

load_dotenv()

API_KEY = os.getenv("API_KEY")
API_KEY_NAME = os.getenv("API_KEY_NAME")
BASE_URL = os.getenv("MEDIA_BASE_URL")

headers = {
    API_KEY_NAME: API_KEY,
}

response = requests.get(
    f"{BASE_URL}/forum/posts?limit=10&offset=0",
    headers=headers,
)

print("Response: ", response.json())
print("Status Code: ", response.status_code)
