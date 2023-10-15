import requests
import glob
from pprint import pprint
import os

# Retrieve the URL of the API and my API key
API_URL = os.getenv("API_URL")
assert API_URL

API_KEY = os.getenv("API_KEY")
assert API_KEY

# Construct the URL of the `/indexes` endpoint
INDEXES_URL = f"{API_URL}/indexes"

# Specify the name of the index
INDEX_NAME = "Content Creator Videos"

# Set the header of the request
headers = {"x-api-key": API_KEY}

# Declare a dictionary named data
data = {
    "engines": [
        {
            "engine_name": "marengo2.5",  # Configure the video understanding engine
            "engine_options": [
                "visual",
                "conversation",
                "text_in_video",
                "logo",
            ],  # Specify the engine options
        },
        {
            "engine_name": "pegasus1",  # Configure the video understanding engine
            "engine_options": ["visual", "conversation"],  # Specify the engine options
        },
    ],
    "index_name": INDEX_NAME,
    "addons": ["thumbnail"],  # Enable the thumbnail generation feature
}

# Create an index
response = requests.post(INDEXES_URL, headers=headers, json=data)

# Store the unique identifier of your index
INDEX_ID = response.json().get("_id")

# Print the status code and response
print(f"Status code: {response.status_code}")
pprint(response.json())
