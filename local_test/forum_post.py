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

data = {
    "content": "This is the content of the new forum post.",
    "author_name": "Author Name",
}

response = requests.post(
    f"{BASE_URL}/forum/posts",
    headers=headers,
    json=data,
)

print("Response: ", response.json())
print("Status Code: ", response.status_code)
